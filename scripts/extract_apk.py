"""
extract_apk.py - Extract vanilla material.bin files from Minecraft APK.

Usage:
    python scripts/extract_apk.py <path_to_apk> [--only NAME ...]

Extracts .material.bin files from the APK to vanilla/android/.
Auto-detects whether materials are at:
    assets/renderer/materials/         (older versions)
    assets/assets/renderer/materials/  (1.21.x split-APK builds)

By default extracts every material. Use --only to limit (e.g. for Phase 1):
    python scripts/extract_apk.py minecraft.apk --only RenderChunk
"""

import argparse
import os
import shutil
import sys
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VANILLA_DIR = PROJECT_ROOT / "vanilla"
ANDROID_DIR = VANILLA_DIR / "android"

CANDIDATE_PREFIXES = (
    "assets/assets/renderer/materials/",
    "assets/renderer/materials/",
)


def detect_prefix(zf: zipfile.ZipFile) -> str:
    names = zf.namelist()
    for prefix in CANDIDATE_PREFIXES:
        if any(n.startswith(prefix) and n.endswith(".material.bin") for n in names):
            return prefix
    return ""


def extract_materials(apk_path: str, only: list[str] | None):
    apk = Path(apk_path)
    if not apk.exists():
        print(f"[ERROR] APK not found: {apk}")
        sys.exit(1)
    if not zipfile.is_zipfile(str(apk)):
        print(f"[ERROR] Not a valid ZIP/APK: {apk}")
        sys.exit(1)

    if ANDROID_DIR.exists():
        shutil.rmtree(ANDROID_DIR)
    ANDROID_DIR.mkdir(parents=True)

    only_set = set(only) if only else None

    with zipfile.ZipFile(str(apk), "r") as zf:
        prefix = detect_prefix(zf)
        if not prefix:
            print("[ERROR] Could not find renderer/materials inside APK.")
            print("        Tried prefixes:")
            for p in CANDIDATE_PREFIXES:
                print(f"          - {p}")
            sys.exit(1)

        print(f"[INFO] Using path prefix: {prefix}")

        count = 0
        for entry in zf.namelist():
            if not (entry.startswith(prefix) and entry.endswith(".material.bin")):
                continue

            filename = os.path.basename(entry)
            stem = filename.replace(".material.bin", "")

            if only_set and stem not in only_set:
                continue

            target = ANDROID_DIR / filename
            with zf.open(entry) as src, open(target, "wb") as dst:
                dst.write(src.read())
            count += 1
            print(f"  Extracted: {filename}")

    print(f"\n[OK] Extracted {count} material.bin file(s) to: {ANDROID_DIR}")
    print("\nNext step: unpack with lazurite:")
    print(f"  lazurite unpack \"{ANDROID_DIR}\" -o \"{ANDROID_DIR}\"")


def main():
    parser = argparse.ArgumentParser(description="Extract material.bin from Minecraft APK")
    parser.add_argument("apk", help="Path to Minecraft APK file")
    parser.add_argument(
        "--only",
        nargs="+",
        metavar="NAME",
        help="Only extract listed materials (without .material.bin extension). "
             "Example: --only RenderChunk Sky",
    )
    args = parser.parse_args()
    extract_materials(args.apk, args.only)


if __name__ == "__main__":
    main()
