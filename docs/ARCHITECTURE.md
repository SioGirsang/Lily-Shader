# Architecture

## Pipeline (Vibrant Visuals)

```
JSON configs in pack/
        |
   [build.py: zip everything]
        |
   Lily-Shader-v{ver}.mcpack
        |
   [User imports to Minecraft]
        |
   [Minecraft loads Vibrant Visuals settings from JSON]
        |
   Effects rendered by Minecraft's built-in deferred renderer
```

No GLSL, no shader compilation, no binary repacking. Minecraft's Vibrant Visuals engine reads our JSON files and applies the settings directly.

## Why This Approach

**Old approach (MaterialBinTool):**
- Reverse-engineered binary `.material.bin` modification
- Required Java, shaderc, MaterialBinTool, MB Loader on Android
- Broken at every Minecraft format change
- Round-trip repack lost data on MC 1.26+ (terrain disappeared)

**New approach (Vibrant Visuals):**
- Official Mojang/Microsoft API
- Pure JSON config
- Stable across game updates
- Works on Windows, Android, iOS, Xbox without launcher

## Directory Structure

```
Lily-Shader/
├── pack/
│   ├── manifest.json              # capabilities: ["pbr"]
│   ├── pack_icon.png
│   │
│   ├── color_grading/
│   │   └── color_grading.json     # ACES tonemap + contrast/saturation/temperature
│   │
│   ├── lighting/
│   │   └── global.json            # Sun/moon illuminance & color (keyframed)
│   │
│   ├── atmospherics/
│   │   └── atmospherics.json      # Sky zenith/horizon, Rayleigh/Mie
│   │
│   ├── water/
│   │   └── water.json             # Waves, caustics, particle concentrations
│   │
│   ├── shadows/
│   │   └── shadows.json           # Soft shadows, texel size
│   │
│   ├── pbr/
│   │   └── global.json            # Fallback MERS for non-PBR textures
│   │
│   ├── local_lighting/
│   │   └── local_lighting.json    # Torch, lantern, end_rod custom colors
│   │
│   └── subpacks/
│       ├── low/                   # Performance preset (overrides)
│       │   ├── color_grading/
│       │   ├── lighting/
│       │   ├── shadows/
│       │   └── water/
│       └── mid/                   # Balanced preset (mirrors defaults)
│           ├── color_grading/
│           ├── lighting/
│           ├── shadows/
│           └── water/
│
├── scripts/
│   └── build.py                   # Zip pack/ into .mcpack
│
├── docs/
│   ├── SETUP.md
│   ├── BUILD.md
│   └── ARCHITECTURE.md
│
└── build/                          # Output (gitignored)
```

## Subpack System

Minecraft's subpack mechanism lets users choose a preset from the resource pack's settings UI. Each subpack folder is a partial overlay:

- Files in `pack/foo/bar.json` are the **default**
- If `pack/subpacks/low/foo/bar.json` exists, it **replaces** the default when "Low" preset is active
- Files NOT overridden in a subpack fall back to the default

This means each preset only specifies what changes, keeping configs minimal.

## Keyframe Animation

Many Vibrant Visuals parameters support keyframes - values that change with time of day:

```json
"illuminance": {
  "0.0": 110000.0,    // Noon: full daylight
  "0.25": 25000.0,    // Sunset
  "0.5": 0.5,         // Midnight: nearly off
  "0.75": 25000.0,    // Sunrise
  "1.0": 110000.0     // Next noon
}
```

Keys are floats from 0 (noon) to 1 (next noon, 24h later). Minecraft linearly interpolates between keys.

Used heavily in `lighting/global.json` and `atmospherics/atmospherics.json` for natural day/night transitions.

## Schema Versions

Each JSON has a `format_version` matching the Minecraft schema it targets:

| File | Schema Version | Why |
|------|----------------|-----|
| color_grading.json | 1.21.90 | Temperature grading added |
| lighting/global.json | 1.26.0 | Keyframe support for ambient/sky |
| atmospherics/atmospherics.json | 1.21.40 | Atmospherics introduced |
| water/water.json | 1.26.0 | biome_water_color_contribution added |
| shadows/shadows.json | 1.21.80 | Shadow customization added |
| pbr/global.json | 1.21.40 | PBR fallback introduced |
| local_lighting/local_lighting.json | 1.21.120 | Replaces old point_lights/ |

`min_engine_version` in manifest is `[1, 21, 120]` to ensure all features are available.

## Maintainability

When Minecraft updates:
- JSON schemas evolve, but old `format_version` values remain supported
- New fields can be added by bumping `format_version` in the affected file
- No reverse engineering needed
- Documentation: https://learn.microsoft.com/en-us/minecraft/creator/documents/vibrantvisuals/

## Future Extensions

Areas to extend in later phases:

- **Per-biome variants**: `atmospherics/end.json`, `water/ocean.json`, etc. with `biomes/*.client_biome.json` references
- **Texture sets**: `textures/blocks/*.texture_set.json` for PBR-aware blocks
- **Volumetric fog**: `fogs/default_fog_settings.json` with media coefficients
- **More subpacks**: Custom variants per-feature (shadows quality, water quality, etc.)
- **Heightmaps**: For displaced surfaces in PBR
