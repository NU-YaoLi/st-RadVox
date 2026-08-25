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

_NONE_TOKENS = {"", "none", "n/a", "na", "nil", "empty", "no", "nothing"}
_NUM_PREFIX_RE = re.compile(r"^\d+[\.\)\-:]\s*")
_DOTTED_KEY_RE = re.compile(r"\b[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*\b")
_LINE_SPLIT_RE = re.compile(r"[,;]+")
_PROSE_STOP = {
    "the", "a", "an", "is", "are", "was", "were", "and", "or", "with", "without",
    "of", "in", "on", "to", "for", "this", "that", "not", "normal", "abnormal",
    "enlarged", "finding", "findings",
}


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


def is_explicit_empty_omit(raw: str | None) -> bool:
    """True when the model explicitly said nothing is abnormal (empty / none / n/a)."""
    if raw is None:
        return False
    return str(raw).strip().lower() in _NONE_TOKENS


def _map_token(token: str, *, valid: set[str], aliases: dict[str, str]) -> str | None:
    t = token.strip().lower()
    t = t.lstrip("-•* ").strip()
    t = t.strip(" .")
    t = _NUM_PREFIX_RE.sub("", t).strip()
    t = re.sub(r"\s+", " ", t)
    if t in _NONE_TOKENS:
        return None
    compact = t.replace(" ", "_")
    dotted = t.replace(" ", "")
    candidates = [t, compact, dotted, t.replace("_", ".")]
    for c in candidates:
        if c in valid:
            return c
        if c in aliases:
            mapped = aliases[c]
            if mapped in valid:
                return mapped
    return None


def parse_omit_keys(raw: str | None, *, valid: set[str], aliases: dict[str, str]) -> set[str]:
    """Parse <omit_template_parts> into validated region.part keys.

    Accepts one key per line, comma/semicolon lists, space-separated dotted keys,
    numbered/bulleted lines, and alias words (spleen → abdomen.spleen).
    """
    if not raw or not str(raw).strip():
        return set()
    text = str(raw).strip().lower()
    if text in _NONE_TOKENS:
        return set()

    found: set[str] = set()

    for match in _DOTTED_KEY_RE.findall(text):
        if match in valid:
            found.add(match)
        elif match in aliases and aliases[match] in valid:
            found.add(aliases[match])

    for line in str(raw).splitlines():
        line = line.strip().lower()
        line = line.lstrip("-•* ").strip()
        line = _NUM_PREFIX_RE.sub("", line).strip()
        if not line or line in _NONE_TOKENS:
            continue
        pieces = [p.strip() for p in _LINE_SPLIT_RE.split(line) if p.strip()]
        if not pieces:
            pieces = [line]
        for piece in pieces:
            mapped = _map_token(piece, valid=valid, aliases=aliases)
            if mapped:
                found.add(mapped)
                continue
            words = piece.split()
            if len(words) <= 1 or any(w in _PROSE_STOP for w in words):
                continue
            for word in words:
                mapped = _map_token(word, valid=valid, aliases=aliases)
                if mapped:
                    found.add(mapped)

    return found


def format_omitted_keys(omit: set[str]) -> str:
    if not omit:
        return "none"
    return ", ".join(sorted(omit))


# Enforced on every radiology report (PDF copy-paste must stay unformatted).
REPORT_PLAIN_TEXT_RULE = """\
PLAIN TEXT OUTPUT (required):
- Write the report as plain text only so it can be pasted into a PDF form without formatting artifacts.
- Do not number any headings or lines (no 1. 2. 3. or 1) 2) 3)).
- Do not use bullets or list markers (no •, -, *, –).
- Do not use markdown or decorative symbols (no **, __, `, #, or similar).
- Section and organ labels may be ordinary words on their own line (Findings, Conclusion, Spleen) followed by
  normal sentences. Do not decorate those labels with numbers or symbols other than a trailing colon.
"""

CONCLUSION_IMPRESSION_RULE = """\
CONCLUSION STYLE (impression list, required for every study, including long or complex ones):
- Output the conclusion heading specified above, then a blank line, then a FLAT list of short impression paragraphs.
  Most significant first, then secondary, then incidental. Do not group conclusions under body-region headers
  (no Thorax: or Abdomen: under conclusions).
- One impression per paragraph. Separate paragraphs with one blank line.
- Each paragraph is a diagnosis or key finding, then a brief interpretation or ranked differential in the SAME
  paragraph. Prefer 1-2 sentences. A third sentence is allowed only for a short differential (primary consideration,
  then what is less likely).
- Do not restate Findings or Diagnostic Interpretation. Do not repeat measurements, technique, or canned normal
  template wording. Do not merge unrelated diagnoses into one dense paragraph.
- Incidental or normal items, if worth listing, are one short line (for example: Aerophagia. Normal head and neck.
  Transitional C7 and T1, incidental.). Skip trivial normals that were not dictated as worth concluding.
- Do not number lines. Do not use bullets or other list markers.
"""


def assemble_region_blocks(
    regions: dict[str, dict[str, str]],
    omit: set[str],
) -> dict[str, str]:
    return {region: assemble_parts(parts, region, omit) for region, parts in regions.items()}
