# Tools Setup

Lily Shader uses **MaterialBinTool** (Java) to unpack and repack RenderDragon `.material.bin` files. Download the tools below into `tools/bin/`.

## Required

### MaterialBinTool.jar

Unpacks and repacks `.material.bin` files. Works with Minecraft 1.21.x material format.

- URL: https://github.com/ddf8196/MaterialBinTool/releases/tag/v0.9.1
- File: `MaterialBinTool-0.9.1-all.jar`
- Save as: `tools/bin/MaterialBinTool.jar`
- Requires: Java JDK 8+

## Optional

### shaderc.exe

bgfx shader compiler. Not used by the current injection pipeline but useful for advanced workflows.

- URL: https://github.com/ddf8196/MaterialBinTool/releases/tag/v0.8.2
- File: `shaderc.exe`
- Save as: `tools/bin/shaderc.exe`

### glslang.exe

GLSL validator. Catches shader errors that would crash Minecraft on Android.

- URL: https://github.com/KhronosGroup/glslang/releases
- File: `glslang-master-windows-x64-Release.zip`
- Extract `bin/glslangValidator.exe`, rename to `glslang.exe`
- Save as: `tools/bin/glslang.exe`

## Folder Structure After Setup

```
tools/
├── README.md
└── bin/
    ├── MaterialBinTool.jar  (required)
    ├── shaderc.exe          (optional)
    └── glslang.exe          (optional)
```

## Verify

```powershell
java -jar tools/bin/MaterialBinTool.jar --help
.\tools\bin\glslang.exe --version
```
