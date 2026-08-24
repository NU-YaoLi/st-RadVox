"""CT prompts — clinic templates for literal normal thorax / normal abdomen + structured report."""

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
- A later report step looks for the exact contiguous phrases **normal thorax** and **normal abdomen** (the word
  normal, one ASCII space, then thorax or abdomen). If the dictation contains either, your polished text MUST still
  include that same two-word sequence in that order with exactly one space (capitalization may follow sentence rules).
  Do not replace a dictated trigger with paraphrases such as "thorax is normal" or "the thorax is unremarkable" if
  that removes the contiguous **normal thorax** or **normal abdomen** pair. (Other wording like "within normal limits"
  elsewhere is fine when it is not replacing those two-word triggers.) Do not insert words between "normal" and the
  anatomical term. Do not add these phrases if they were not dictated.
"""

THORAX_PARTS: dict[str, str] = {
    "pulmonary": (
        "Minimal, unstructured ground glass attenuation is noted in the dependent aspect of the pulmonary parenchyma, "
        "without nodules or masses. The airways are normal, without wall thickness or luminal collapse."
    ),
    "cardiac": (
        "The cardiac chambers are normal, without dilation or an overt impression of wall thickening or thinning. "
        "The pulmonary vessels and great vessels are appropriate in size and morphology, without congestion."
    ),
    "mediastinum": (
        "The mediastinal and pleural spaces are within normal limits, without lymphadenopathy, mass lesions, or "
        "effusion. An incidental thymic remnant is noted in the cranioventral mediastinum."
    ),
    "cranial_abdomen": (
        "The collimated cranial abdomen is normal, without nodules or mass lesions, lymphadenopathy, or effusion."
    ),
    "osseous": "The osseous structures and external soft tissues are unremarkable.",
}

ABDOMEN_PARTS: dict[str, str] = {
    "hepatic": (
        "The hepatic parenchyma is normal in attenuation and contrast enhancement, without nodules or masses. The "
        "gallbladder is normal in shape and size, with a small amount of incidental, hyperattenuating sludge. No "
        "biliary dilation is appreciated. The hepatic and portal vasculature is normal. At the porta hepatis, the "
        "hepatic lymph nodes are normal in size and appearance, measuring [X] mm."
    ),
    "splenic": (
        "The splenic parenchyma is normal in attenuation and contrast enhancement, without nodules or masses. The "
        "associated vasculature and lymph node are within normal limits."
    ),
    "pancreatic": (
        "The pancreatic parenchyma is normal in attenuation and contrast enhancement, without thickening or "
        "surrounding fat standing. The pancreaticoduodenal lymph node is small and normal."
    ),
    "gastrointestinal": (
        "The gastrointestinal tract is normal, with a small amount of luminal content noted in the stomach, without "
        "gastric wall thickening. Normal pyloric duodenal junction. Normal small intestines without an impression of "
        "generalized or regional wall thickening or architectural alteration. Normal ileocolic junction and large "
        "intestines. The jejunal and colic lymph nodes are appropriate, measuring [X] mm."
    ),
    "urogenital": (
        "Bilaterally, the kidneys are normal and symmetrical in shape, size, margination, attenuation, and "
        "enhancement. No ureteral dilation is noted. The urinary bladder is normal, containing homogeneous urine, "
        "and without wall thickening or irregularity."
    ),
    "adrenals": (
        "The adrenal glands are within normal limits, measuring [X] mm at the caudal pole on the left and [X] mm on "
        "the right."
    ),
    "peritoneal": "No peritoneal or retroperitoneal effusion or fat stranding is evident.",
    "caudal_thorax": "The collimated caudal thorax is within normal limits.",
    "osseous": "The osseous structures and external soft tissues are unremarkable.",
}

TEMPLATE_REGIONS = {"thorax": THORAX_PARTS, "abdomen": ABDOMEN_PARTS}

OMIT_ALIASES = {
    "pulmonary": "thorax.pulmonary",
    "lung": "thorax.pulmonary",
    "lungs": "thorax.pulmonary",
    "airway": "thorax.pulmonary",
    "airways": "thorax.pulmonary",
    "cardiac": "thorax.cardiac",
    "heart": "thorax.cardiac",
    "mediastinum": "thorax.mediastinum",
    "pleural": "thorax.mediastinum",
    "pleura": "thorax.mediastinum",
    "cranial_abdomen": "thorax.cranial_abdomen",
    "cranial abdomen": "thorax.cranial_abdomen",
    "thorax.osseous": "thorax.osseous",
    "hepatic": "abdomen.hepatic",
    "liver": "abdomen.hepatic",
    "gallbladder": "abdomen.hepatic",
    "splenic": "abdomen.splenic",
    "spleen": "abdomen.splenic",
    "pancreatic": "abdomen.pancreatic",
    "pancreas": "abdomen.pancreatic",
    "gastrointestinal": "abdomen.gastrointestinal",
    "gi": "abdomen.gastrointestinal",
    "stomach": "abdomen.gastrointestinal",
    "intestines": "abdomen.gastrointestinal",
    "urogenital": "abdomen.urogenital",
    "kidney": "abdomen.urogenital",
    "kidneys": "abdomen.urogenital",
    "renal": "abdomen.urogenital",
    "bladder": "abdomen.urogenital",
    "adrenals": "abdomen.adrenals",
    "adrenal": "abdomen.adrenals",
    "peritoneal": "abdomen.peritoneal",
    "retroperitoneal": "abdomen.peritoneal",
    "caudal_thorax": "abdomen.caudal_thorax",
    "caudal thorax": "abdomen.caudal_thorax",
    "abdomen.osseous": "abdomen.osseous",
}

TEMPLATE_PART_GUIDE = """\
- thorax.pulmonary: lungs, pulmonary parenchyma, airways
- thorax.cardiac: heart, cardiac chambers, pulmonary and great vessels
- thorax.mediastinum: mediastinum, pleural space, thymus
- thorax.cranial_abdomen: collimated cranial abdomen on the thoracic study
- thorax.osseous: thoracic osseous structures and external soft tissues
- abdomen.hepatic: liver, gallbladder, biliary tree, hepatic lymph nodes
- abdomen.splenic: spleen / splenic parenchyma
- abdomen.pancreatic: pancreas
- abdomen.gastrointestinal: GI tract, stomach, intestines, jejunal/colic lymph nodes
- abdomen.urogenital: kidneys, ureters, urinary bladder
- abdomen.adrenals: adrenal glands
- abdomen.peritoneal: peritoneal / retroperitoneal spaces
- abdomen.caudal_thorax: collimated caudal thorax on the abdominal study
- abdomen.osseous: abdominal osseous structures and external soft tissues
"""


def valid_omit_keys() -> set[str]:
    return valid_keys_from_regions(TEMPLATE_REGIONS)


def assemble_templates(omit: set[str]) -> dict[str, str]:
    return assemble_region_blocks(TEMPLATE_REGIONS, omit)


REPORT_TASK = (
    "Format the provided professional clinical text into a structured CT Radiology Report using "
    "Diagnostic Interpretation and Conclusions. Apply the already-pruned institutional normal thorax/abdomen "
    "paragraphs when triggers in the rules fire (including dictation_template_cues from raw transcript); replace "
    "every [X] in the abdomen template using numerals dictated in the professional clinical text when provided."
)


def get_report_rules(region_blocks: dict[str, str], omitted_keys: set[str]) -> str:
    thorax_block = (region_blocks.get("thorax") or "").strip()
    abdomen_block = (region_blocks.get("abdomen") or "").strip()
    omitted = format_omitted_keys(omitted_keys)

    if thorax_block:
        thorax_rule = f"""\
3. When the **normal thorax** trigger applies, under Diagnostic Interpretation output **Thorax:** on its own line,
   then a blank line, then paste EXACTLY the following already-pruned institutional paragraph block (including blank
   lines). Do not add/remove remaining sentences. Do not restore omitted parts as normal.
{thorax_block}
"""
    else:
        thorax_rule = """\
3. Do NOT insert the institutional **normal thorax** block (cue absent, or every thorax part was omitted as abnormal).
   Describe any thoracic abnormalities from **source** under **Thorax:** using the Diagnostic Interpretation pattern.
"""

    if abdomen_block:
        abdomen_rule = f"""\
4. When the **normal abdomen** trigger applies, output a single **Abdomen:** subsection (heading on its own line,
   then a blank line, then the paragraph), using the already-pruned institutional text below, except that every token
   **[X]** must be replaced as follows:
   - If **source** states an explicit measurement for that slot (e.g. hepatic lymph nodes 5 mm, adrenal left 4 mm),
     substitute the dictated number and unit (mm or cm) for that **[X]**.
   - If **source** lists structured measurements (e.g. after "normal abdomen with the following measurements"),
     map each dictated value into the anatomically matching **[X]** in the template when unambiguous.
   - If a value for a given **[X]** was not dictated, replace only that **[X]** with: **not specified in dictation**
     (do not invent numbers).

   Then paste EXACTLY the following already-pruned institutional paragraph block, with every **[X]** substituted:
{abdomen_block}

   If both thorax and abdomen template blocks are present, output **Thorax:** first, then **Abdomen:**, separated by
   one blank line. After the pruned templates, describe omitted/abnormal parts from **source** under the matching
   region heading (do not paste normal canned text for them).
"""
    else:
        abdomen_rule = """\
4. Do NOT insert the institutional **normal abdomen** block (cue absent, or every abdomen part was omitted as
   abnormal). Describe abdominal abnormalities from **source** under **Abdomen:**.
"""

    return f"""\
OUTPUT RULES (must follow exactly):

Let **source** mean the provided professional clinical text.
Let **cues** mean the text inside the XML tag <dictation_template_cues> in the same input (may be empty). Each
non-empty line of **cues** is a canonical cue detected from the raw transcript (e.g. a line exactly `normal thorax`).

1. Use ONLY these two sections, in this order: **Diagnostic Interpretation** and **Conclusions**.

2. TEMPLATE TRIGGERS (CT) — **professional_clinical_text** and/or **dictation_template_cues**
   - **normal thorax** template: apply the pruned thorax block in rule 3 if (a) **source** contains the
     case-insensitive substring **normal thorax** (word "normal", ASCII space, word "thorax"), OR (b) **cues**
     contains its own line exactly `normal thorax`. Do not use synonyms or paraphrases alone.
   - **normal abdomen** template (with [X] handling in rule 4): apply the pruned abdomen block if (a) **source**
     contains the substring **normal abdomen**, OR (b) **cues** contains its own line exactly `normal abdomen`.
   - Abnormal parts were already removed from the blocks below. Never add those organs back as normal canned text.
   - Omitted (abnormal) parts: {omitted}

{thorax_rule}
{abdomen_rule}
5. DIAGNOSTIC INTERPRETATION — structure
   - Output the heading **Diagnostic Interpretation** on its own line, then one blank line.
   - Immediately after that, in order: optional **Thorax:** template block (rule 3), optional **Abdomen:** template
     block (rule 4), then any additional body-region subsections from **source** (each header ending with a colon,
     followed by ONE paragraph; no bullets in this section), including omitted/abnormal organs.
   - If neither template block is present, write Diagnostic Interpretation only from **source** using the same
     region-colon-paragraph pattern.
   - Omit regions with no relevant findings.

6. CONCLUSIONS
   - Heading **Conclusions** on its own line, then a blank line.
   - Under each region that has conclusions, a region header ending with a colon, then ONLY bullet lines prefixed
     with "• " (no paragraphs under the region).
   - Leave one blank line between region blocks and between Diagnostic Interpretation and Conclusions.

7. Do not output angle-bracket placeholders like "<Body Region 1>" in the final text.
8. Keep content specific and anatomical. Do not add extraneous sections (e.g., history, technique).
9. Ensure to use Oxford comma to separate any continuous adjectives in a sentence.
"""
