# Lily Shader

A realistic shader for Minecraft Bedrock Edition (RenderDragon) with PBR support.

![Version](https://img.shields.io/badge/version-0.1.0--alpha-blue)
![Minecraft](https://img.shields.io/badge/Minecraft-1.21.x-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

## Features

- **ACES Filmic Tonemap** - cinematic color grading
- **Scalable Presets** - Low, Mid, and Custom variants
- **Mobile Optimized** - designed for Android low-end to mid-range devices
- **Auto-injection Pipeline** - modular system for adding shader effects

### Planned Features (Roadmap)

- [ ] PBR support (LabPBR format, SUSPENDED/YSS compatible)
- [ ] Dynamic shadows
- [ ] Realistic water with reflections
- [ ] Volumetric clouds
- [ ] Bloom/Glow effects
- [ ] Waving plants
- [ ] Motion blur (optional)

## Requirements

### For Users
- Minecraft Bedrock 1.21.x+
- Android: [MB Loader](https://play.google.com/store/apps/details?id=io.github.bambosan.mbloader)
- Windows: [BetterRenderDragon](https://github.com/QYCottage/BetterRenderDragon)

### For Developers
- Python 3.10+
- Java JDK 8+
- MaterialBinTool v0.9.1

## Installation

1. Download the latest `.mcpack` from [Releases](https://github.com/SioGirsang/Lily-Shader/releases)
2. Install MB Loader (Android) or BetterRenderDragon (Windows)
3. Import the `.mcpack` into Minecraft
4. Enable the resource pack and select your preferred preset

## Building from Source

See [docs/SETUP.md](docs/SETUP.md) for full development environment setup.

```bash
# Extract vanilla materials from APK
python scripts/extract_apk.py <path_to_minecraft.apk>

# Unpack materials with MaterialBinTool
java -jar tools/bin/MaterialBinTool.jar -u vanilla/android/RenderChunk.material.bin -o vanilla/mbt

# Build all main presets (low + mid)
python scripts/build.py

# Build specific preset
python scripts/build.py --preset mid

# Build all presets including custom variants
python scripts/build.py --all
```

## Presets

| Preset | Exposure | Saturation | Contrast | Target Device |
|--------|----------|------------|----------|---------------|
| Low    | 1.05     | 1.04       | 1.02     | Low-end       |
| Mid    | 1.15     | 1.08       | 1.04     | Mid-range     |
| Custom | Per-feature configurable via subpack selection |

## Architecture

```
Vanilla .material.bin
        |
   [MaterialBinTool unpack]
        |
   Vanilla GLSL shaders
        |
   [inject.py: inject effect code]
        |
   Modified GLSL shaders
        |
   [MaterialBinTool repack]
        |
   Modified .material.bin
        |
   [build.py: package]
        |
   Lily-Shader-v{ver}-{preset}.mcpack
```

## License

MIT License - see [LICENSE](LICENSE)

## Credits

- **Author**: SioGirsang
- **Tools**: [MaterialBinTool](https://github.com/ddf8196/MaterialBinTool)
- **Reference**: [Newb X Legacy](https://github.com/devendrn/newb-x-mcbe), [RenderDragonSourceCodeInv](https://github.com/SurvivalApparatusCommunication/RenderDragonSourceCodeInv)
