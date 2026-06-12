"""
build.py - Bundle Lily Shader resource pack into .mcpack

Usage:
    python scripts/build.py [--version VERSION]

Creates a .mcpack file (zip) from the pack/ directory.
No compilation needed - Vibrant Visuals uses JSON configs directly.
"""

import argparse
import zipfile
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PACK_DIR = PROJECT_ROOT / "pack"
BUILD_DIR = PROJECT_ROOT / "build"


def build_mcpack(version: str) -> Path:
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    mcpack_name = f"Lily-Shader-v{version}.mcpack"
    mcpack_path = BUILD_DIR / mcpack_name

    with zipfile.ZipFile(str(mcpack_path), "w", zipfile.ZIP_DEFLATED) as zf:
        for file in PACK_DIR.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(PACK_DIR).as_posix()
                zf.write(str(file), arcname)

    size_kb = mcpack_path.stat().st_size / 1024
    print(f"[OK] {mcpack_name} ({size_kb:.1f} KB)")
    return mcpack_path


def main():
    parser = argparse.ArgumentParser(description="Bundle Lily Shader .mcpack")
    parser.add_argument("--version", default="0.2.0-alpha",
                        help="Version string for output filename")
    args = parser.parse_args()

    result = build_mcpack(args.version)
    print(f"Output: {result}")


if __name__ == "__main__":
    main()
