"""Split institutional normal templates into named parts and prune abnormal ones."""

from __future__ import annotations

import re

# Cue phrase (from raw transcript) -> region key used in prompt modules.
CUE_TO_REGION = {
    "normal thorax": "thorax",
    "normal abdomen": "abdomen",
    "normal brain": "brain",
    "normal spine": "spine",
}

_TOKEN_SPLIT = re.compile(r"[\n,;]+")
_NONE_TOKENS = {"", "none", "n/a", "na", "nil", "empty", "no", "nothing"}


def full_part_key(region: str, part: str) -> str:
    return f"{region}.{part}"


def part_is_omitted(region: str, part: str, omit: set[str]) -> bool:
    """True if the model listed this part as abnormal (bare or region-qualified)."""
    return part in omit or full_part_key(region, part) in omit


def valid_keys_from_regions(regions: dict[str, dict[str, str]]) -> set[str]:
    return {full_part_key(region, part) for region, parts in regions.items() for part in parts}


def assemble_parts(parts: dict[str, str], region: str, omit: set[str]) -> str:
    """Join remaining institutional paragraphs with a blank line; skip omitted parts."""
    kept: list[str] = []
    for part, text in parts.items():
        if part_is_omitted(region, part, omit):
            continue
        chunk = (text or "").strip()
        if chunk:
            kept.append(chunk)
    return "\n\n".join(kept)


def parse_omit_keys(raw: str | None, *, valid: set[str], aliases: dict[str, str]) -> set[str]:
    """Parse <omit_template_parts> into validated region.part keys."""
    if not raw or not str(raw).strip():
        return set()
    text = str(raw).strip().lower()
    if text in _NONE_TOKENS:
        return set()

    found: set[str] = set()
    for token in _TOKEN_SPLIT.split(str(raw)):
        t = token.strip().lower()
        t = t.lstrip("-•* ").strip()
        t = t.strip(" .")
        t = re.sub(r"\s+", " ", t)
        if t in _NONE_TOKENS:
            continue
        compact = t.replace(" ", "_")
        dotted = t.replace(" ", "")
        candidates = [t, compact, dotted, t.replace("_", ".")]
        mapped: str | None = None
        for c in candidates:
            if c in valid:
                mapped = c
                break
            if c in aliases:
                mapped = aliases[c]
                break
        if mapped in valid:
            found.add(mapped)
    return found


def format_omitted_keys(omit: set[str]) -> str:
    if not omit:
        return "none"
    return ", ".join(sorted(omit))


def assemble_region_blocks(
    regions: dict[str, dict[str, str]],
    omit: set[str],
) -> dict[str, str]:
    return {region: assemble_parts(parts, region, omit) for region, parts in regions.items()}
