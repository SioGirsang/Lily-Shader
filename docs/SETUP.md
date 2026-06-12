# Development Environment Setup

Lily Shader is a pure JSON resource pack for Minecraft Bedrock's **Vibrant Visuals** pipeline. No compilation, no Java, no third-party shader tools.

## Prerequisites

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Git** - [Download](https://git-scm.com/)
- A text editor (VS Code recommended)

## Step 1: Clone Repository

```bash
git clone https://github.com/SioGirsang/Lily-Shader.git
cd Lily-Shader
```

## Step 2: Build

```bash
python scripts/build.py
```

Output: `build/Lily-Shader-v{version}.mcpack`

That's it. No tool downloads needed.

## Step 3: Test in Minecraft

1. Transfer `.mcpack` to your device
2. Open it - Minecraft auto-imports
3. Enable Vibrant Visuals: **Settings > Video > Graphics Mode > Vibrant Visuals**
4. Apply pack via Global Resources or per-world settings
5. Select preset (Low or Mid)

## Editing Configs

All shader behavior is controlled by JSON files in `pack/`. Edit them with any text editor:

| File | Controls |
|------|----------|
| `color_grading/color_grading.json` | Tone mapping, contrast, saturation, color temperature |
| `lighting/global.json` | Sun/moon brightness and color (with day/night keyframes) |
| `atmospherics/atmospherics.json` | Sky color, scattering, sun glare |
| `water/water.json` | Wave depth, octaves, speed, caustics |
| `shadows/shadows.json` | Shadow style (soft/blocky), texel size |
| `pbr/global.json` | Default metalness/emissive/roughness fallback |
| `local_lighting/local_lighting.json` | Custom colors for torches, lanterns, etc |

After editing, run `python scripts/build.py` to repackage.

## Schema References

Microsoft's official schemas describe every available field:
- https://learn.microsoft.com/en-us/minecraft/creator/documents/vibrantvisuals/

## Troubleshooting

### Vibrant Visuals option missing in Minecraft
Your device may not support deferred rendering. The pack installs but effects won't render. Try a more recent device, or check if a Minecraft update enables your device.

### Pack imports but effects don't apply
- Verify Vibrant Visuals is **ON** in video settings (this is required)
- Verify the pack is **applied** (Global Resources or in-world resource list)
- Check that `min_engine_version` in your Minecraft is 1.21.120 or higher

### JSON validation
The build script will fail loudly if any JSON has syntax errors. To check manually:

```bash
python -c "import json; json.load(open('pack/color_grading/color_grading.json'))"
```
