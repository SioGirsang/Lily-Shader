# Development Environment Setup

## Prerequisites

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Java JDK 8+** - [Download](https://adoptium.net/)
- **Git** - [Download](https://git-scm.com/)

## Step 1: Clone Repository

```bash
git clone https://github.com/SioGirsang/Lily-Shader.git
cd Lily-Shader
```

## Step 2: Download MaterialBinTool

1. Go to: https://github.com/ddf8196/MaterialBinTool/releases/tag/v0.9.1
2. Download `MaterialBinTool-0.9.1-all.jar`
3. Place in `tools/bin/MaterialBinTool.jar`

## Step 3: Download shaderc.exe (Optional, for validation)

1. Go to: https://github.com/ddf8196/MaterialBinTool/releases/tag/v0.8.2
2. Download `shaderc.exe`
3. Place in `tools/bin/shaderc.exe`

## Step 4: Download glslang (Optional, for GLSL validation)

1. Go to: https://github.com/KhronosGroup/glslang/releases
2. Download `glslang-master-windows-x64-Release.zip`
3. Extract `bin/glslangValidator.exe`
4. Rename to `glslang.exe` and place in `tools/bin/glslang.exe`

## Step 5: Extract Vanilla Materials from Minecraft APK

### Getting the APK from Android

1. Open **ZArchiver** on your Android device
2. Navigate to one of:
   - `/data/app/~~XXXX/com.mojang.minecraftpe-XXXX/base.apk`
   - Or your Downloads folder if you have the APK
3. **Copy** `base.apk` to `/sdcard/Download/minecraft.apk`
4. Transfer to your PC via USB or cloud storage

### Extract Materials

```bash
# Extract .material.bin files from APK
python scripts/extract_apk.py path/to/minecraft.apk

# Unpack with MaterialBinTool
java -jar tools/bin/MaterialBinTool.jar -u vanilla/android/RenderChunk.material.bin -o vanilla/mbt
```

## Step 6: Verify Setup

```bash
# Build the mid preset
python scripts/build.py --preset mid

# Check output
dir build/
```

You should see:
- `Lily-Shader-v0.1.0-alpha-mid.mcpack`

## Folder Structure After Setup

```
Lily-Shader/
├── tools/bin/
│   ├── MaterialBinTool.jar  ✓
│   ├── shaderc.exe          (optional)
│   └── glslang.exe          (optional)
├── vanilla/
│   ├── android/
│   │   └── RenderChunk.material.bin
│   └── mbt/
│       └── RenderChunk/     (unpacked)
└── build/
    └── Lily-Shader-v0.1.0-alpha-mid.mcpack
```

## Troubleshooting

### "MaterialBinTool.jar not found"
Ensure `tools/bin/MaterialBinTool.jar` exists.

### "Java not found"
Install JDK 8+ and ensure `java` is in your PATH.

### "Vanilla unpacked materials not found"
Run the extract and unpack steps first (Step 5).

### Shader doesn't work in-game
- Ensure MB Loader (Android) or BetterRenderDragon (Windows) is installed
- Check that the resource pack is enabled in Global Resources
- Try restarting Minecraft after enabling
