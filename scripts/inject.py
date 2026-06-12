"""
inject.py - Inject Lily Shader code into vanilla GLSL fragment shaders.

The injection model:
  Each fragment file in src/fragments/ has two sections separated by the
  marker line:
      ---LILY_SPLIT---
  - Section 1 (above the marker): helper functions, injected just before
    'void main(){' in the target shader.
  - Section 2 (below the marker): apply calls, injected just before the
    last 'bgfx_FragColor = ...' assignment in main().

Macros from the preset are prepended as #define lines before Section 1.

Only ESSL fragment shaders are touched. Vertex shaders are passed through
unchanged.
"""

import re
import shutil
from pathlib import Path
from typing import Iterable

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_FRAGMENTS = PROJECT_ROOT / "src" / "fragments"

SPLIT_MARKER = "---LILY_SPLIT---"
MAIN_PATTERN = re.compile(r"\nvoid\s+main\s*\(\s*\)\s*\{")
OUTPUT_PATTERN = re.compile(
    r"^([ \t]*)(bgfx_FragColor\s*=\s*[^;]+;)",
    re.MULTILINE,
)


def load_fragment(name: str) -> tuple[str, str]:
    """Load src/fragments/<name>.glsl and split into (helpers, apply)."""
    path = SRC_FRAGMENTS / f"{name}.glsl"
    if not path.exists():
        raise FileNotFoundError(f"Fragment not found: {path}")

    text = path.read_text(encoding="utf-8")
    if SPLIT_MARKER not in text:
        raise ValueError(f"Fragment {name} missing {SPLIT_MARKER}")

    helpers, apply = text.split(SPLIT_MARKER, 1)
    return helpers.strip("\n"), apply.strip("\n")


def build_macro_block(macros: dict[str, str]) -> str:
    if not macros:
        return ""
    lines = [f"#define {k} {v}" for k, v in macros.items()]
    return "\n".join(lines)


def inject_fragment_shader(
    glsl: str, features: Iterable[str], macros: dict[str, str]
) -> str:
    """Inject helpers + apply calls into one ESSL fragment shader."""
    feature_list = list(features)
    if not feature_list:
        return glsl

    helpers_blocks: list[str] = []
    apply_blocks: list[str] = []
    for feat in feature_list:
        helpers, apply = load_fragment(feat)
        helpers_blocks.append(helpers)
        apply_blocks.append(apply)

    macro_block = build_macro_block(macros)

    helpers_text = (
        "\n// === LILY HELPERS START ===\n"
        + (macro_block + "\n\n" if macro_block else "")
        + "\n\n".join(helpers_blocks)
        + "\n// === LILY HELPERS END ===\n"
    )

    apply_text = (
        "\n    // === LILY APPLY START ===\n"
        + "\n".join(apply_blocks)
        + "\n    // === LILY APPLY END ===\n"
    )

    main_match = MAIN_PATTERN.search(glsl)
    if not main_match:
        return glsl

    glsl = (
        glsl[: main_match.start()]
        + helpers_text
        + glsl[main_match.start() :]
    )

    output_matches = list(OUTPUT_PATTERN.finditer(glsl))
    if not output_matches:
        return glsl

    last = output_matches[-1]
    glsl = glsl[: last.start()] + apply_text + glsl[last.start() :]

    return glsl


# Passes that only write to depth buffer, not color buffer.
# Injecting color grading here breaks rendering on some GPUs.
SKIP_PASSES = {"DepthOnly", "DepthOnlyOpaque"}


def is_target_fragment(file: Path) -> bool:
    """We only inject into ESSL_310 fragment shaders for color passes.

    Skips depth-only passes which write only to the depth buffer.
    """
    name = file.name
    if not (name.endswith(".Fragment.glsl") and "ESSL_310" in name):
        return False

    # Pass name is the parent directory (e.g. .../Opaque/0.ESSL_310.Fragment.glsl)
    pass_name = file.parent.name
    if pass_name in SKIP_PASSES:
        return False

    return True


def process_material_dir(
    material_dir: Path, features: Iterable[str], macros: dict[str, str]
) -> int:
    """Walk a material dir and inject into every ESSL_310 fragment shader.

    Returns the count of files modified.
    """
    count = 0
    for path in material_dir.rglob("*.Fragment.glsl"):
        if not is_target_fragment(path):
            continue

        original = path.read_text(encoding="utf-8")
        modified = inject_fragment_shader(original, features, macros)
        if modified != original:
            path.write_text(modified, encoding="utf-8")
            count += 1
    return count


def copy_material_for_preset(
    src_unpacked: Path, dst_root: Path, material: str
) -> Path:
    """Copy unpacked material from vanilla into a preset-specific working dir."""
    src = src_unpacked / material
    if not src.exists():
        raise FileNotFoundError(f"Unpacked material not found: {src}")

    dst = dst_root / material
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(str(src), str(dst))
    return dst
