// ============================================================================
// Lily Shader - Color Grading Fragment
//
// Two sections separated by the marker line:
//   [Section 1] helper functions  -> injected before "void main(){"
//   [Section 2] apply call         -> injected before the fragment output line
//
// Preset macros (LILY_EXPOSURE, LILY_SATURATION, LILY_CONTRAST) are prepended
// automatically by scripts/inject.py based on the selected preset.
// ============================================================================

// ACES Filmic Tonemap (Narkowicz approximation)
vec3 lilyTonemapACES(vec3 x) {
    const float a = 2.51;
    const float b = 0.03;
    const float c = 2.43;
    const float d = 0.59;
    const float e = 0.14;
    return clamp((x * (a * x + b)) / (x * (c * x + d) + e), 0.0, 1.0);
}

float lilyLuma(vec3 c) {
    return dot(c, vec3(0.2126, 0.7152, 0.0722));
}

vec3 lilySaturation(vec3 c, float amount) {
    float l = lilyLuma(c);
    return mix(vec3(l, l, l), c, amount);
}

vec3 lilyContrast(vec3 c, float amount) {
    return (c - 0.5) * amount + 0.5;
}

vec3 lilyGrade(vec3 color) {
    color = pow(color, vec3(2.2));
    color *= LILY_EXPOSURE;
    color = lilyTonemapACES(color);
    color = lilySaturation(color, LILY_SATURATION);
    color = lilyContrast(color, LILY_CONTRAST);
    color = pow(clamp(color, 0.0, 1.0), vec3(1.0 / 2.2));
    return color;
}

// ---LILY_SPLIT---

    fragmentOutput.Color0.rgb = lilyGrade(fragmentOutput.Color0.rgb);
