# Build Guide

## Quick Build

```bash
# Build main presets (low + mid)
python scripts/build.py

# Build specific preset
python scripts/build.py --preset mid

# Build all presets including custom variants
python scripts/build.py --all

# Build with specific version
python scripts/build.py --preset mid --version 0.2.0
```

## Build Pipeline

The build process has 4 stages:

```
1. Copy     - Copy vanilla unpacked material to working directory
2. Inject   - Inject Lily shader code into fragment shaders
3. Repack   - Repack into .material.bin using MaterialBinTool
4. Package  - Bundle into .mcpack with manifest and assets
```

## Available Presets

### Main Presets
- `low` - minimal color grading, best performance
- `mid` - balanced color grading (recommended)

### Custom Variants (for future features)
- `custom_shadows_off`, `custom_shadows_low`, `custom_shadows_high`
- `custom_water_simple`, `custom_water_full`
- `custom_bloom_off`, `custom_bloom_on`
- `custom_clouds_simple`, `custom_clouds_full`
- `custom_pbr_off`, `custom_pbr_on`
- `custom_motionblur_off`, `custom_motionblur_on`

## Build Output

```
build/
├── work/                    # Working directory (injected shaders)
│   └── mid/
│       └── RenderChunk/
├── materials/               # Repacked .material.bin files
│   └── mid/
│       └── RenderChunk.material.bin
├── stage/                   # Staging for .mcpack creation
└── Lily-Shader-v0.1.0-alpha-mid.mcpack
```

## Adding New Effects

1. Create a new fragment file in `src/fragments/`:
   ```
   src/fragments/bloom.glsl
   ```

2. Use the split marker to separate helpers from apply code:
   ```glsl
   // Helper functions here
   vec3 applyBloom(vec3 color) { ... }

   // ---LILY_SPLIT---

       fragmentOutput.Color0.rgb = applyBloom(fragmentOutput.Color0.rgb);
   ```

3. Register the feature in `scripts/presets.py`:
   ```python
   FEATURE_MATERIALS = {
       "grading": ["RenderChunk"],
       "bloom": ["RenderChunk"],  # Add this
   }
   ```

4. Add to preset features:
   ```python
   "mid": {
       "macros": { ... },
       "features": ["grading", "bloom"],
   },
   ```

## Validating GLSL

Use glslang to validate shaders before testing on device:

```bash
# Validate a specific shader
.\tools\bin\glslang.exe -S frag build\work\mid\RenderChunk\Opaque\0.ESSL_310.Fragment.glsl
```

No output = valid GLSL.

## Troubleshooting

### "Repacking failed"
- Check that Java is installed and `java` command works
- Verify `tools/bin/MaterialBinTool.jar` exists

### "Injected into 0 fragment shader(s)"
- Ensure vanilla materials are unpacked in `vanilla/mbt/`
- Check that the material name in `FEATURE_MATERIALS` matches the folder name

### mcpack file is very small
- Check that `pack/manifest.json` exists
- Verify materials were repacked successfully
