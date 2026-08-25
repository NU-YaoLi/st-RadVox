"""Prompts for plain radiograph (survey radiography) — clinic normal paragraphs from templates.docx (Radiographs)."""

from __future__ import annotations

from .radvox_bknd_templates import (
    CONCLUSION_IMPRESSION_RULE,
    REPORT_PLAIN_TEXT_RULE,
    assemble_parts,
    format_omitted_keys,
    part_is_omitted,
    valid_keys_from_regions,
)

PRO_TASK = (
    "Convert the transcribed veterinary radiology dictation into a highly polished, professional clinical version "
    "suitable for official records or doctor-to-doctor communication."
)

PRO_RULES = """\
OUTPUT RULES:
- Preserve all newlines and structural formatting from the original text.
- Use a double line break (\\n\\n) to create an empty line between the description and the impressions.
- Ensure that any continuous adjectives in a sentence are strictly separated by a comma.
  Example: "An ill-defined roughly triangular cranioventral thoracic soft tissue opacity" ->
  "An ill-defined, roughly, triangular, cranioventral, thoracic, soft tissue opacity".
- A later report step looks for the exact contiguous phrases **normal thorax** and **normal abdomen** (the word
  normal, one ASCII space, then thorax or abdomen). If the dictation contains either, your polished text MUST still
  include that same two-word sequence in that order with exactly one space (capitalization may follow sentence rules).
  Do not rephrase into forms that remove the pair, such as "thorax is normal" or "the abdomen is unremarkable", if that
  loses the contiguous **normal thorax** / **normal abdomen** wording. Do not insert words between "normal" and the
  anatomical term. Do not add these phrases if they were not dictated.
"""

THORAX_PARTS: dict[str, str] = {
    "pulmonary": (
        "The pulmonary parenchyma is within normal limits, without nodules, masses, regions of consolidation, or "
        "abnormal lung patterns."
    ),
    "cardiac": (
        "The cardiac silhouette is normal, without generalized or specific chamber enlargement. The pulmonary "
        "vessels and great vessels are appropriate in size and morphology, without congestion."
    ),
    "mediastinum": (
        "The mediastinal and pleural spaces are within normal limits. Mild, dynamic caudal esophageal fluid is noted "
        "on the left lateral view, consistent with incidental passive reflux."
    ),
    "cranial_abdomen": "The collimated cranial abdomen is normal, with preserved serosal detail.",
    "osseous": "The osseous structures and external soft tissues are unremarkable.",
}

# Viscera are one institutional sentence; prune individual organs then rebuild the list.
_VISCERA_ORIGINAL = (
    "The visible hepatic, splenic, renal, and urinary bladder silhouettes are within normal limits for shape, size, "
    "margination, and opacity."
)
_VISCERA_ORDER: tuple[tuple[str, str], ...] = (
    ("hepatic", "hepatic"),
    ("splenic", "splenic"),
    ("renal", "renal"),
    ("urinary_bladder", "urinary bladder"),
)

ABDOMEN_FIXED_PARTS: dict[str, str] = {
    "gastrointestinal": (
        "The stomach is normal in size, containing mild, unstructured, heterogeneous, fluid and gas content, which "
        "exhibits appropriate redistribution into the pylorus on the left lateral view, suggesting patency at the "
        "time of imaging. The small intestines consist of a homogeneous population, without dilation or plication. "
        "The large intestines are within normal limits, containing gas and heterogeneous, formed fecal content."
    ),
    "peritoneal": "The serosal detail of the peritoneal and retroperitoneal spaces is preserved.",
    "caudal_thorax": "The collimated caudal thorax is unremarkable.",
    "osseous": "The osseous structures and external soft tissues are unremarkable.",
}

# Dummy texts so valid_omit_keys includes viscera organs; assemble_templates rebuilds that sentence.
_VISCERA_PLACEHOLDERS = {key: "" for key, _label in _VISCERA_ORDER}

TEMPLATE_REGIONS = {
    "thorax": THORAX_PARTS,
    "abdomen": {**ABDOMEN_FIXED_PARTS, **_VISCERA_PLACEHOLDERS},
}

OMIT_ALIASES = {
    "pulmonary": "thorax.pulmonary",
    "lung": "thorax.pulmonary",
    "lungs": "thorax.pulmonary",
    "cardiac": "thorax.cardiac",
    "heart": "thorax.cardiac",
    "mediastinum": "thorax.mediastinum",
    "pleural": "thorax.mediastinum",
    "pleura": "thorax.mediastinum",
    "esophagus": "thorax.mediastinum",
    "cranial_abdomen": "thorax.cranial_abdomen",
    "cranial abdomen": "thorax.cranial_abdomen",
    "thorax.osseous": "thorax.osseous",
    "gastrointestinal": "abdomen.gastrointestinal",
    "gi": "abdomen.gastrointestinal",
    "stomach": "abdomen.gastrointestinal",
    "intestines": "abdomen.gastrointestinal",
    "hepatic": "abdomen.hepatic",
    "liver": "abdomen.hepatic",
    "splenic": "abdomen.splenic",
    "spleen": "abdomen.splenic",
    "renal": "abdomen.renal",
    "kidney": "abdomen.renal",
    "kidneys": "abdomen.renal",
    "urinary_bladder": "abdomen.urinary_bladder",
    "bladder": "abdomen.urinary_bladder",
    "urinary bladder": "abdomen.urinary_bladder",
    "peritoneal": "abdomen.peritoneal",
    "retroperitoneal": "abdomen.peritoneal",
    "serosal": "abdomen.peritoneal",
    "caudal_thorax": "abdomen.caudal_thorax",
    "caudal thorax": "abdomen.caudal_thorax",
    "abdomen.osseous": "abdomen.osseous",
}

TEMPLATE_PART_GUIDE = """\
- thorax.pulmonary: lungs / pulmonary parenchyma
- thorax.cardiac: cardiac silhouette, pulmonary and great vessels
- thorax.mediastinum: mediastinum, pleural space, caudal esophagus
- thorax.cranial_abdomen: collimated cranial abdomen on the thoracic study
- thorax.osseous: thoracic osseous structures and external soft tissues
- abdomen.gastrointestinal: stomach, small intestines, large intestines
- abdomen.hepatic: hepatic silhouette
- abdomen.splenic: splenic silhouette
- abdomen.renal: renal silhouettes
- abdomen.urinary_bladder: urinary bladder silhouette
- abdomen.peritoneal: peritoneal / retroperitoneal serosal detail
- abdomen.caudal_thorax: collimated caudal thorax on the abdominal study
- abdomen.osseous: abdominal osseous structures and external soft tissues
"""


def valid_omit_keys() -> set[str]:
    return valid_keys_from_regions(TEMPLATE_REGIONS)


def _viscera_paragraph(omit: set[str]) -> str:
    kept = [label for key, label in _VISCERA_ORDER if not part_is_omitted("abdomen", key, omit)]
    if not kept:
        return ""
    if len(kept) == 4:
        return _VISCERA_ORIGINAL
    if len(kept) == 1:
        return (
            f"The visible {kept[0]} silhouette is within normal limits for shape, size, margination, and opacity."
        )
    if len(kept) == 2:
        joined = f"{kept[0]} and {kept[1]}"
    else:
        joined = f"{', '.join(kept[:-1])}, and {kept[-1]}"
    return (
        f"The visible {joined} silhouettes are within normal limits for shape, size, margination, and opacity."
    )


def assemble_templates(omit: set[str]) -> dict[str, str]:
    thorax = assemble_parts(THORAX_PARTS, "thorax", omit)
    chunks: list[str] = []
    if not part_is_omitted("abdomen", "gastrointestinal", omit):
        chunks.append(ABDOMEN_FIXED_PARTS["gastrointestinal"].strip())
    viscera = _viscera_paragraph(omit)
    if viscera:
        chunks.append(viscera)
    for key in ("peritoneal", "caudal_thorax", "osseous"):
        if not part_is_omitted("abdomen", key, omit):
            chunks.append(ABDOMEN_FIXED_PARTS[key].strip())
    return {"thorax": thorax, "abdomen": "\n\n".join(chunks)}


REPORT_TASK = (
    "Format the provided professional clinical text into a structured plain radiograph report. "
    "Use Findings plus Conclusion (singular). Apply the already-pruned institutional normal thorax/abdomen "
    "paragraphs only when the source text contains the literal phrases specified in the rules "
    "(case-insensitive substring match)."
)


def get_report_rules(region_blocks: dict[str, str], omitted_keys: set[str]) -> str:
    thorax_block = (region_blocks.get("thorax") or "").strip()
    abdomen_block = (region_blocks.get("abdomen") or "").strip()
    omitted = format_omitted_keys(omitted_keys)

    if thorax_block:
        thorax_paste = f"""\
   - When the thorax rule fires, under Findings output a subsection: a line **Thorax:** then a blank line, then paste
     EXACTLY the following already-pruned institutional paragraph block (including blank lines). Do not add/remove
     remaining sentences. Do not restore omitted parts as normal:
{thorax_block}
"""
    else:
        thorax_paste = """\
   - Do NOT insert the institutional **normal thorax** block (cue absent, or every thorax part was omitted as
     abnormal). Describe thoracic abnormalities from **source** under **Thorax:**.
"""

    if abdomen_block:
        abdomen_paste = f"""\
   - When the abdomen rule fires, under Findings output a subsection: a line **Abdomen:** then a blank line, then paste
     EXACTLY the following already-pruned institutional paragraph block (including blank lines). Do not add/remove
     remaining sentences:
{abdomen_block}

   - If both thorax and abdomen template blocks are present, output **Thorax:** first, then **Abdomen:**, each
     separated by one blank line. After the pruned templates, describe omitted/abnormal parts from **source** (do not
     paste canned normal text for them).
"""
    else:
        abdomen_paste = """\
   - Do NOT insert the institutional **normal abdomen** block (cue absent, or every abdomen part was omitted as
     abnormal). Describe abdominal abnormalities from **source** under **Abdomen:**.
"""

    return f"""\
OUTPUT RULES (must follow exactly):

1. Use ONLY these two sections: "Findings" and "Conclusion".

2. The report MUST follow the structure below (headings, colons, blank lines). Do NOT include bracket placeholders
   like "[Organ System...]" in the output.

3. TEMPLATE TRIGGERS (Radiographs) — **professional_clinical_text** and/or **dictation_template_cues**
   - Let **source** mean the provided professional clinical text.
   - Let **cues** mean the text inside the XML tag <dictation_template_cues> in the same input (may be empty). Each
     non-empty line of **cues** is a canonical cue from the raw transcript (e.g. `normal thorax`).
   - Use the pruned **thorax** paragraph in Findings if (a) **source** contains the case-insensitive substring
     **normal thorax**, OR (b) **cues** contains its own line exactly `normal thorax`. Do NOT use this paragraph
     based on synonyms or paraphrases alone.
   - Use the pruned **abdomen** paragraph in Findings if (a) **source** contains the substring **normal abdomen**,
     OR (b) **cues** contains its own line exactly `normal abdomen`.
   - Abnormal parts were already removed from the blocks below. Never add those organs back as normal canned text.
   - Omitted (abnormal) parts: {omitted}
{thorax_paste}
{abdomen_paste}
4. FINDINGS — remainder of the section
   - Begin Findings with the heading **Findings** on its own line, then a blank line.
   - After any Thorax:/Abdomen: template blocks from rule 3, add other regions, projections, or abnormalities from
     **source** using subheadings that MUST end with a colon (e.g., "Musculoskeletal:", "Additional:", "Spleen:").
   - Under each such subheading (other than the verbatim template paragraphs above), write ONE plain paragraph.
   - If neither template block is present, write Findings only from **source** using the same subheading + paragraph
     conventions; do not invent the institutional normal paragraphs.
   - Include blocks ONLY for regions or topics explicitly mentioned in **source**. Do NOT add filler blocks for
     unmentioned regions.
   - Leave exactly one blank line between distinct subsections under Findings.

5. CONCLUSION
   After one blank line following the Findings section, output the word Conclusion on its own line, then a blank
   line, then impression paragraphs.
{CONCLUSION_IMPRESSION_RULE}

6. Keep content specific and anatomical. Do not add extraneous sections (e.g., history, technique).
7. Ensure to use Oxford comma to separate any continuous adjectives in a sentence.

{REPORT_PLAIN_TEXT_RULE}
"""
