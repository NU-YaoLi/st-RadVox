"""MRI prompts — clinic templates for literal normal brain / normal spine + structured report."""

from __future__ import annotations

from .radvox_bknd_templates import assemble_region_blocks, format_omitted_keys, valid_keys_from_regions

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
- A later report step looks for the exact contiguous phrases **normal brain** and **normal spine** (the word normal,
  one ASCII space, then brain or spine). If the dictation contains either, your polished text MUST still include that
  two-word sequence in that order with exactly one space (capitalization may follow sentence rules). Do not rephrase
  into forms that remove the pair, such as "brain is normal" or "spine unremarkable", if that loses the contiguous
  **normal brain** / **normal spine** wording. Do not insert words between "normal" and the anatomical term. Do not add
  these phrases if they were not dictated.
"""

BRAIN_PARTS: dict[str, str] = {
    "parenchyma": (
        "The cerebral, midbrain, cerebellar, and brain stem structures are all within normal limits for signal "
        "intensity and structural symmetry, without abnormal contrast enhancement. No susceptibility artifact is "
        "noted on GRE images, and no restriction of diffusion is noted on DWI images. The ventricular system is "
        "normal, without dilation. The visible cranial nerves are normal and symmetrical. No midline shift or brain "
        "herniation is present."
    ),
    "extra_cranial": (
        "The extra-cranial osseous structures and soft tissues are within normal limits, with normal and symmetrical "
        "mandibular and medial retropharyngeal lymph nodes."
    ),
}

SPINE_PARTS: dict[str, str] = {
    "structures": (
        "The vertebral bodies, intervertebral disc spaces, articular process joints, and all remaining osseous "
        "structures and paravertebral soft tissues are within normal limits. The intervertebral discs demonstrate "
        "appropriate T2 hyperintensity, without evidence of degeneration, protrusion, or extrusion. No abnormal "
        "contrast enhancement is appreciated."
    ),
}

TEMPLATE_REGIONS = {"brain": BRAIN_PARTS, "spine": SPINE_PARTS}

OMIT_ALIASES = {
    "parenchyma": "brain.parenchyma",
    "brain": "brain.parenchyma",
    "cerebrum": "brain.parenchyma",
    "cerebellum": "brain.parenchyma",
    "brainstem": "brain.parenchyma",
    "brain stem": "brain.parenchyma",
    "ventricle": "brain.parenchyma",
    "ventricles": "brain.parenchyma",
    "extra_cranial": "brain.extra_cranial",
    "extra-cranial": "brain.extra_cranial",
    "extracranial": "brain.extra_cranial",
    "retropharyngeal": "brain.extra_cranial",
    "mandibular lymph nodes": "brain.extra_cranial",
    "structures": "spine.structures",
    "spine": "spine.structures",
    "spinal": "spine.structures",
    "vertebra": "spine.structures",
    "vertebrae": "spine.structures",
    "disc": "spine.structures",
    "discs": "spine.structures",
    "paravertebral": "spine.structures",
}

TEMPLATE_PART_GUIDE = """\
- brain.parenchyma: brain parenchyma, ventricles, cranial nerves, herniation/midline shift
- brain.extra_cranial: extra-cranial osseous/soft tissues, mandibular and medial retropharyngeal lymph nodes
- spine.structures: vertebral bodies, discs, articular process joints, paravertebral soft tissues (omit this whole
  part if ANY spinal finding is abnormal)
"""


def valid_omit_keys() -> set[str]:
    return valid_keys_from_regions(TEMPLATE_REGIONS)


def assemble_templates(omit: set[str]) -> dict[str, str]:
    return assemble_region_blocks(TEMPLATE_REGIONS, omit)


REPORT_TASK = (
    "Format the provided professional clinical text into an MRI report with Findings and Conclusion. "
    "Apply the already-pruned institutional normal brain / normal spine template paragraphs only when the literal "
    "triggers in the rules are present."
)


def get_report_rules(region_blocks: dict[str, str], omitted_keys: set[str]) -> str:
    brain_block = (region_blocks.get("brain") or "").strip()
    spine_block = (region_blocks.get("spine") or "").strip()
    omitted = format_omitted_keys(omitted_keys)

    if brain_block:
        brain_rule = f"""\
3. When the **normal brain** rule fires, under Findings output **Brain:** on its own line, a blank line, then this
   already-pruned institutional paragraph block (including blank lines). Do not add/remove remaining sentences:
{brain_block}
"""
    else:
        brain_rule = """\
3. Do NOT insert the institutional **normal brain** block (cue absent, or every brain part was omitted as abnormal).
   Describe brain abnormalities from **source** under **Brain:**.
"""

    if spine_block:
        spine_rule = f"""\
4. When the **normal spine** rule fires, under Findings output **Spine:** on its own line, a blank line, then this
   already-pruned institutional paragraph block (including blank lines). Do not add/remove remaining sentences:
{spine_block}

   If both brain and spine template blocks are present, output **Brain:** first, then **Spine:**, separated by one
   blank line. After pruned templates, describe omitted/abnormal parts from **source** (do not restore canned normal
   text for them).
"""
    else:
        spine_rule = """\
4. Do NOT insert the institutional **normal spine** block (cue absent, or the spine part was omitted as abnormal).
   Describe spinal abnormalities from **source** under **Spine:**.
"""

    return f"""\
OUTPUT RULES (must follow exactly):

Let **source** mean the provided professional clinical text.
Let **cues** mean the text inside the XML tag <dictation_template_cues> in the same input (may be empty). Each
non-empty line of **cues** is a canonical cue from the raw transcript (e.g. `normal brain`).

1. Use ONLY these two sections: **Findings** and **Conclusion**.

2. TEMPLATE TRIGGERS (MRI) — **source** and/or **dictation_template_cues**
   - Insert the pruned **normal brain** block if (a) **source** contains the case-insensitive substring
     **normal brain**, OR (b) **cues** contains its own line exactly `normal brain`. No synonyms or paraphrases alone.
   - Insert the pruned **normal spine** block if (a) **source** contains the substring **normal spine**,
     OR (b) **cues** contains its own line exactly `normal spine`.
   - Abnormal parts were already removed from the blocks below. Never add those structures back as normal canned text.
   - Omitted (abnormal) parts: {omitted}

{brain_rule}
{spine_rule}
5. FINDINGS — structure
   - Heading **Findings** on its own line, then one blank line.
   - Then optional template blocks from rules 3–4 in order.
   - Then any additional MRI-related subsections from **source** (e.g., omitted/abnormal regions, soft tissues,
     contrast phases) using headings ending with a colon, followed by ONLY bullet lines prefixed with "• " unless
     the template already used a paragraph block above.
   - If neither template block is present, write Findings only from **source** with colon headings and bullets as above.
   - Leave one blank line between distinct subsections under Findings.

6. CONCLUSION
   Conclusion
   1. <Summary of the primary abnormality>. <Clinical interpretation or prioritized differential diagnoses>.
   2. <Summary of a secondary abnormality or incidental finding>. <Interpretation of the finding>.
   3. <Summary of remaining observations, often noting a lack of metastasis or normal general status>.

   Ground each line in **source**.

7. Keep content specific and anatomical. Do not add extraneous sections (e.g., history, technique).
8. Ensure to use Oxford comma to separate any continuous adjectives in a sentence.
"""
