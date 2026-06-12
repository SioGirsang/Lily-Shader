# Architecture

## Overview

Lily Shader uses **MaterialBinTool** to unpack vanilla shaders, **inject.py** to insert effect code, then repack into a distributable `.mcpack`.

```
┌─────────────────────┐
│  Minecraft APK      │
│  (.material.bin)    │
└─────────┬───────────┘
          │ extract_apk.py
          ▼
┌─────────────────────┐
│  vanilla/android/   │
│  RenderChunk.bin    │
└─────────┬───────────┘
          │ MaterialBinTool -u (unpack)
          ▼
┌─────────────────────┐
│  vanilla/mbt/       │
│  RenderChunk/       │
│    Opaque/          │
│      0.ESSL_310.    │
│        Fragment.glsl│
└─────────┬───────────┘
          │ build.py → inject.py
          ▼
┌─────────────────────┐
│  build/work/{preset}│
│  (injected GLSL)    │
└─────────┬───────────┘
          │ MaterialBinTool -r (repack)
          ▼
┌─────────────────────┐
│  build/materials/   │
│  RenderChunk.bin    │
└─────────┬───────────┘
          │ build.py (package)
          ▼
┌─────────────────────┐
│  Lily-Shader-       │
│  v0.1.0-mid.mcpack  │
└─────────────────────┘
```

## Directory Structure

```
Lily-Shader/
├── src/
│   └── fragments/           # Effect code snippets
│       └── grading.glsl     # Color grading (tonemap, saturation, contrast)
│
├── scripts/
│   ├── build.py             # Main build orchestrator
│   ├── inject.py            # GLSL injection engine
│   ├── presets.py           # Preset definitions & macros
│   └── extract_apk.py       # APK material extractor
│
├── vanilla/
│   ├── android/             # Extracted .material.bin (gitignored)
│   └── mbt/                 # Unpacked materials (gitignored)
│
├── pack/
│   ├── manifest.json        # Resource pack manifest
│   ├── pack_icon.png        # Pack icon
│   └── subpacks/            # Preset subpack folders
│
├── tools/bin/
│   ├── MaterialBinTool.jar  # Unpack/repack tool
│   ├── shaderc.exe          # bgfx compiler (optional)
│   └── glslang.exe          # GLSL validator (optional)
│
└── build/                   # Build output (gitignored)
```

## Injection System

### Fragment Files

Each effect is a `.glsl` file in `src/fragments/` with two sections:

```glsl
// Section 1: Helper functions (injected before main())
vec3 myEffect(vec3 color) {
    return color * 1.5;
}

// ---LILY_SPLIT---

// Section 2: Apply call (injected before bgfx_FragColor assignment)
    fragmentOutput.Color0.rgb = myEffect(fragmentOutput.Color0.rgb);
```

### Injection Points

1. **Helpers** - Injected just before `void main(){`
2. **Apply** - Injected just before `bgfx_FragColor = fragmentOutput.Color0;`

### Macros

Preset macros are prepended as `#define` statements:

```glsl
// === LILY HELPERS START ===
#define LILY_EXPOSURE 1.15
#define LILY_SATURATION 1.08
#define LILY_CONTRAST 1.04

vec3 lilyGrade(vec3 color) { ... }
// === LILY HELPERS END ===
```

## Preset System

Presets are defined in `scripts/presets.py`:

```python
PRESETS = {
    "mid": {
        "macros": {
            "LILY_EXPOSURE": "1.15",
            "LILY_SATURATION": "1.08",
            "LILY_CONTRAST": "1.04",
        },
        "features": ["grading"],
    },
}
```

### Inheritance

Presets can inherit from a base:

```python
"custom_bloom_on": {
    "base": "mid",
    "features": ["grading", "bloom"],
}
```

## Materials

### RenderChunk

The main terrain material. Handles:
- Block textures
- Lightmap
- Fog
- **Lily additions**: ACES tonemap, color grading

Passes: `Opaque`, `AlphaTest`, `Transparent`, `DepthOnly`, `DepthOnlyOpaque`

### Future Materials

- `Sky` - sky gradient, atmosphere
- `Clouds` / `CloudsForwardPBR` - cloud rendering
- `WaterForwardPBR` - water surface
- `SunMoon` - sun and moon
- `Stars` - night sky stars

## Maintainability

When Minecraft updates:

1. Extract new vanilla materials from updated APK
2. Unpack with MaterialBinTool
3. Check for structural changes (new passes, renamed uniforms)
4. Rebuild - injection system adapts automatically if structure unchanged
5. Test on device

The injection approach is resilient because it targets specific patterns (`void main()` and `bgfx_FragColor`) rather than line numbers.
