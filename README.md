# Lily Shader

A realistic shader for Minecraft Bedrock Edition using **Vibrant Visuals** (official Mojang PBR pipeline).

![Version](https://img.shields.io/badge/version-0.2.0--alpha-blue)
![Minecraft](https://img.shields.io/badge/Minecraft-1.21.120%2B-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

## Features

- **ACES Filmic Tonemap** for cinematic color
- **Dynamic Lighting** with realistic sun/moon illuminance throughout the day
- **Atmospheric Sky** with Rayleigh/Mie scattering and time-of-day color shifts
- **Soft Shadows** with proper shadow mapping
- **Animated Water** with waves and caustics
- **Custom Point Lights** for torches, lanterns, and glowing blocks
- **PBR Texture Support** (LabPBR-like, compatible with SUSPENDED/Flavor texture packs)
- **No launcher needed** - works as a standard resource pack

## Why Vibrant Visuals?

Lily Shader uses Minecraft's **official Vibrant Visuals** system instead of third-party tools like MaterialBinTool. This means:

- No MB Loader / BetterRenderDragon required
- Cross-platform: Windows, Android, iOS, Xbox
- Stable across game updates
- Fully supported by Mojang/Microsoft

## Requirements

### For Users
- Minecraft Bedrock Edition **1.21.120** or later
- Device that supports Vibrant Visuals
- Vibrant Visuals enabled in: **Settings > Video > Graphics Mode > Vibrant Visuals**

### Device Compatibility
- Snapdragon 8s Gen 3 / 8 Gen 1+ (Adreno): Fully supported
- Mid to high-end MediaTek (Mali-G77+): Generally supported
- Older / low-end devices: Vibrant Visuals option may not appear; in that case the pack installs but effects do not render

## Installation

1. Download `Lily-Shader-v{version}.mcpack` from [Releases](https://github.com/SioGirsang/Lily-Shader/releases)
2. Open the file - Minecraft will import it automatically
3. In Minecraft: **Settings > Video > Graphics Mode > Vibrant Visuals** (must be ON)
4. Apply the resource pack to your world or in Global Resources
5. Pick a preset: **Low - Performance** or **Mid - Balanced**

## Presets

| Preset | Tonemap | Shadows | Water Waves | Caustics | Sky Keyframes | Target |
|--------|---------|---------|-------------|----------|---------------|--------|
| Low    | ACES (subtle) | Blocky | 8 octaves | Off | Static | Low-end |
| Mid    | ACES (full) | Soft | 24 octaves | On | Animated | Mid-range+ |

## Building from Source

```bash
# Clone the repo
git clone https://github.com/SioGirsang/Lily-Shader.git
cd Lily-Shader

# Build the .mcpack
python scripts/build.py

# Output: build/Lily-Shader-v{version}.mcpack
```

No external tools (Java, MaterialBinTool, shaderc) required. Just Python's standard library.

## Project Structure

```
Lily-Shader/
├── pack/
│   ├── manifest.json              # PBR capability declaration
│   ├── color_grading/             # ACES tonemap, contrast, saturation
│   ├── lighting/                  # Sun, moon, ambient (with keyframes)
│   ├── atmospherics/              # Sky color, Rayleigh/Mie scattering
│   ├── water/                     # Waves, caustics
│   ├── shadows/                   # Soft shadow settings
│   ├── pbr/                       # Fallback MER values
│   ├── local_lighting/            # Torch, lantern, glowstone colors
│   └── subpacks/
│       ├── low/                   # Low preset overrides
│       └── mid/                   # Mid preset overrides
├── scripts/
│   └── build.py                   # Bundle pack into .mcpack
└── docs/
    ├── SETUP.md
    ├── BUILD.md
    └── ARCHITECTURE.md
```

## License

MIT License - see [LICENSE](LICENSE)

## Credits

- **Author**: SioGirsang
- **Pipeline**: Microsoft / Mojang Vibrant Visuals
- **Reference docs**: https://learn.microsoft.com/en-us/minecraft/creator/documents/vibrantvisuals/
