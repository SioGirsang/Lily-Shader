"""
build.py - Main build script for Lily Shader.

Pipeline:
  1. Unpack vanilla material.bin (MaterialBinTool)
  2. Copy unpacked material to working directory
  3. Inject Lily shader code into fragment shaders
  4. Repack into .material.bin (MaterialBinTool)
  5. Bundle into .mcpack

Usage:
    python scripts/build.py [--preset PRESET] [--version VERSION]
    python scripts/build.py --preset mid
    python scripts/build.py  (builds all presets)
"""

import argparse
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from inject import copy_material_for_preset, process_material_dir
from presets import FEATURE_MATERIALS, all_preset_names, resolve_preset

TOOLS_BIN = PROJECT_ROOT / "tools" / "bin"
MBT_JAR = TOOLS_BIN / "MaterialBinTool.jar"
VANILLA_UNPACKED = PROJECT_ROOT / "vanilla" / "mbt"
BUILD_DIR = PROJECT_ROOT / "build"
PACK_DIR = PROJECT_ROOT / "pack"


def check_tools():
    if not MBT_JAR.exists():
        print(f"[ERROR] MaterialBinTool.jar not found at: {MBT_JAR}")
        print("  Download from: https://github.com/ddf8196/MaterialBinTool/releases/tag/v0.9.1")
        sys.exit(1)

    result = subprocess.run(["java", "-version"], capture_output=True, text=True)
    if result.returncode != 0:
        print("[ERROR] Java not found. Install JDK 8+.")
        sys.exit(1)


def check_vanilla():
    if not VANILLA_UNPACKED.exists() or not any(VANILLA_UNPACKED.iterdir()):
        print("[ERROR] Vanilla unpacked materials not found.")
        print("  Run first:")
        print(f'    python scripts/extract_apk.py <path_to_apk>')
        print(f'    java -jar tools/bin/MaterialBinTool.jar -u vanilla/android/RenderChunk.material.bin -o vanilla/mbt')
        sys.exit(1)


def repack_material(working_dir: Path, output_dir: Path, material: str):
    """Repack a material folder back into .material.bin using MaterialBinTool."""
    output_dir.mkdir(parents=True, exist_ok=True)
    material_path = working_dir / material

    cmd = [
        "java", "-jar", str(MBT_JAR),
        "-r", str(material_path),
        "-o", str(output_dir),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [ERROR] Repack failed for {material}")
        print(f"  stdout: {result.stdout}")
        print(f"  stderr: {result.stderr}")
        return False

    bin_file = output_dir / f"{material}.material.bin"
    if bin_file.exists():
        print(f"  [OK] Repacked: {bin_file.name} ({bin_file.stat().st_size / 1024:.1f} KB)")
        return True
    else:
        print(f"  [ERROR] Output file not found: {bin_file}")
        return False


def create_mcpack(preset_name: str, version: str, materials_dir: Path) -> Path | None:
    """Bundle materials + pack/ into a .mcpack file."""
    stage_dir = BUILD_DIR / "stage" / preset_name
    if stage_dir.exists():
        shutil.rmtree(stage_dir)
    stage_dir.mkdir(parents=True)

    shutil.copytree(str(PACK_DIR), str(stage_dir / "pack_content"), dirs_exist_ok=True)

    dest_mats = stage_dir / "pack_content" / "renderer" / "materials"
    dest_mats.mkdir(parents=True, exist_ok=True)

    for f in materials_dir.glob("*.material.bin"):
        shutil.copy2(str(f), str(dest_mats / f.name))

    mcpack_name = f"Lily-Shader-v{version}-{preset_name}.mcpack"
    mcpack_path = BUILD_DIR / mcpack_name

    with zipfile.ZipFile(str(mcpack_path), "w", zipfile.ZIP_DEFLATED) as zf:
        pack_root = stage_dir / "pack_content"
        for file in pack_root.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(pack_root).as_posix()
                zf.write(str(file), arcname)

    print(f"  [OK] Created: {mcpack_name} ({mcpack_path.stat().st_size / 1024:.1f} KB)")
    return mcpack_path


def build_preset(preset_name: str, version: str) -> bool:
    """Build one preset: copy vanilla → inject → repack → mcpack."""
    print(f"\n{'='*60}")
    print(f"  Building preset: {preset_name}")
    print(f"{'='*60}")

    preset = resolve_preset(preset_name)
    macros = preset["macros"]
    features = preset["features"]

    working_dir = BUILD_DIR / "work" / preset_name
    if working_dir.exists():
        shutil.rmtree(working_dir)
    working_dir.mkdir(parents=True)

    materials_output = BUILD_DIR / "materials" / preset_name
    if materials_output.exists():
        shutil.rmtree(materials_output)
    materials_output.mkdir(parents=True)

    materials_to_process = set()
    for feat in features:
        if feat in FEATURE_MATERIALS:
            materials_to_process.update(FEATURE_MATERIALS[feat])

    success = True
    for material in materials_to_process:
        print(f"\n  Processing: {material}")

        try:
            mat_dir = copy_material_for_preset(VANILLA_UNPACKED, working_dir, material)
        except FileNotFoundError as e:
            print(f"  [ERROR] {e}")
            success = False
            continue

        count = process_material_dir(mat_dir, features, macros)
        print(f"  Injected into {count} fragment shader(s)")

        if not repack_material(working_dir, materials_output, material):
            success = False
            continue

    if success:
        create_mcpack(preset_name, version, materials_output)

    return success


def main():
    parser = argparse.ArgumentParser(description="Build Lily Shader")
    parser.add_argument("--preset", default=None,
                        help="Build specific preset (default: low + mid only)")
    parser.add_argument("--version", default="0.1.0-alpha",
                        help="Version string for output filename")
    parser.add_argument("--all", action="store_true",
                        help="Build all presets including custom variants")
    args = parser.parse_args()

    check_tools()
    check_vanilla()

    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    if args.preset:
        targets = [args.preset]
    elif args.all:
        targets = all_preset_names()
    else:
        targets = ["low", "mid"]

    success = 0
    for name in targets:
        try:
            if build_preset(name, args.version):
                success += 1
        except Exception as e:
            print(f"  [ERROR] {name}: {e}")

    print(f"\n{'='*60}")
    print(f"  Build complete: {success}/{len(targets)} presets")
    print(f"  Output: {BUILD_DIR}")
    print(f"{'='*60}")

    if success == 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
