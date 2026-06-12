"""
presets.py - Preset definitions for Lily Shader.

Each preset maps to a set of GLSL macro values that are prepended to the
injected shader code. Feature toggles control which effect fragments get
injected.
"""

PRESETS = {
    "low": {
        "macros": {
            "LILY_EXPOSURE": "1.05",
            "LILY_SATURATION": "1.04",
            "LILY_CONTRAST": "1.02",
        },
        "features": ["grading"],
    },
    "mid": {
        "macros": {
            "LILY_EXPOSURE": "1.15",
            "LILY_SATURATION": "1.08",
            "LILY_CONTRAST": "1.04",
        },
        "features": ["grading"],
    },
    "custom_shadows_off":   {"base": "mid", "features": ["grading"]},
    "custom_shadows_low":   {"base": "mid", "features": ["grading"]},
    "custom_shadows_high":  {"base": "mid", "features": ["grading"]},
    "custom_water_simple":  {"base": "mid", "features": ["grading"]},
    "custom_water_full":    {"base": "mid", "features": ["grading"]},
    "custom_bloom_off":     {"base": "mid", "features": ["grading"]},
    "custom_bloom_on":      {"base": "mid", "features": ["grading"]},
    "custom_clouds_simple": {"base": "mid", "features": ["grading"]},
    "custom_clouds_full":   {"base": "mid", "features": ["grading"]},
    "custom_pbr_off":       {"base": "mid", "features": ["grading"]},
    "custom_pbr_on":        {"base": "mid", "features": ["grading"]},
    "custom_motionblur_off":{"base": "mid", "features": ["grading"]},
    "custom_motionblur_on": {"base": "mid", "features": ["grading"]},
}

# Which materials each feature applies to.
FEATURE_MATERIALS = {
    "grading": ["RenderChunk"],
}


def resolve_preset(name: str) -> dict:
    """Resolve a preset, following 'base' inheritance."""
    if name not in PRESETS:
        raise KeyError(f"Unknown preset: {name}")

    preset = dict(PRESETS[name])
    base_name = preset.get("base")
    if base_name:
        base = resolve_preset(base_name)
        macros = dict(base["macros"])
        macros.update(preset.get("macros", {}))
        preset["macros"] = macros
        if "features" not in preset:
            preset["features"] = base["features"]
    return preset


def all_preset_names() -> list[str]:
    return list(PRESETS.keys())
