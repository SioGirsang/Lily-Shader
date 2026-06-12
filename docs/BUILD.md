# Build Guide

Building Lily Shader is just bundling JSON files into a `.mcpack` (which is a zip).

## Quick Build

```bash
python scripts/build.py
```

Output: `build/Lily-Shader-v0.2.0-alpha.mcpack`

## Custom Version

```bash
python scripts/build.py --version 0.3.0
```

Output: `build/Lily-Shader-v0.3.0.mcpack`

## What the Build Does

1. Reads everything in `pack/`
2. Creates a zip archive with `.mcpack` extension
3. Done - no compilation, no shader generation

## Adding New Effects

Vibrant Visuals supports many JSON-based effect categories. To add or modify:

1. Edit/create the relevant JSON in `pack/<category>/`
2. Reference Microsoft's docs for schema details:
   https://learn.microsoft.com/en-us/minecraft/creator/documents/vibrantvisuals/
3. Run `python scripts/build.py`
4. Test in Minecraft

## Adding a Preset Subpack

Subpacks let users pick a preset from the resource pack's settings.

1. Add the subpack entry in `pack/manifest.json`:
   ```json
   "subpacks": [
     { "folder_name": "ultra", "name": "Ultra", "memory_tier": 2 }
   ]
   ```

2. Create the override folder:
   ```
   pack/subpacks/ultra/
       color_grading/color_grading.json
       lighting/global.json
       water/water.json
   ```

3. Only include the JSON files you want to override - other files fall back to the defaults in `pack/`

4. Build and test

## Testing JSON Validity

```bash
# Check all JSON files in the pack
python -c "import json,glob; [json.load(open(f)) for f in glob.glob('pack/**/*.json', recursive=True)]; print('All valid')"
```

## Output Location

All builds go to `build/`. Files there are gitignored. Versioned releases should be tagged in git.
