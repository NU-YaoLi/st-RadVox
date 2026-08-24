"""US prompts — clinic normal-abdomen template + standard abdominal US report."""

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
- A later report step looks for the exact contiguous phrase **normal abdomen** (the word normal, one ASCII space,
  then abdomen). If the dictation contains it, your polished text MUST still include that two-word sequence in that
  order with exactly one space (capitalization may follow sentence rules). Do not rephrase into "abdomen is normal",
  "abdominal structures are unremarkable", or similar if that removes the contiguous **normal abdomen** pair. Do not
  insert words between "normal" and "abdomen". Do not add this phrase if it was not dictated.
"""

ABDOMEN_PARTS: dict[str, str] = {
    "hepatobiliary": (
        "Hepatobiliary system:\n"
        "The hepatic parenchyma is within normal limits for shape, size, echogenicity, and echotexture, without "
        "nodules or masses. Preserved portal markings. The gallbladder is normal, containing anechoic bile and a "
        "small amount of incidental, unstructured, echogenic sludge. No gallbladder wall thickening or biliary "
        "dilation is evident. At the porta hepatis, no lymphadenomegaly is noted, and the portal vessel is normal "
        "upon evaluation with spectral Doppler."
    ),
    "spleen": (
        "Spleen:\n"
        "The splenic parenchyma is within normal limits for shape, size, echogenicity, and echotexture, without "
        "nodules or masses. Normal splenic vascularity is noted with color Doppler evaluation."
    ),
    "pancreas": (
        "Pancreas:\n"
        "The pancreas is normal in thickness and echogenicity, without surrounding hyperechogenicity."
    ),
    "gastrointestinal": (
        "Gastrointestinal tract:\n"
        "The stomach is normal in size, containing a small amount of gas, causing a mild reverberation artifact, "
        "mildly limiting visualization of the dorsal wall. The visible aspects of the gastric walls and the pyloric "
        "duodenal junction are within normal limits. The small intestines are traced, with normal wall architecture "
        "and thicknesses noted:  duodenum [X] mm, jejunum [X] mm, and ileum [X] mm. The ileocolic junction and large "
        "intestines are normal, with colonic wall thickness of [X] mm."
    ),
    "urogenital": (
        "Urogenital system:\n"
        "Bilaterally, the kidneys are normal and symmetrical in shape, size, margination, and corticomedullary "
        "definition, measuring [X] cm in length on the left and [X] cm on the right. No renal pelvic dilation or "
        "perirenal hyperechogenicity is noted. The urinary bladder is normal, containing anechoic urine, and without "
        "wall thickening or irregularity."
    ),
    "adrenals": (
        "Adrenal glands:\n"
        "The adrenal glands are within normal limits, measuring [X] mm at the caudal pole on the left and [X] mm on "
        "the right."
    ),
    "lymph_nodes": (
        "Lymph nodes:\n"
        "The jejunal and colic lymph nodes are normal, measuring [X] mm and [X] mm respectively. The medial iliac "
        "lymph nodes are symmetrical and normal, measuring [X] mm on the left and [X] mm on the right."
    ),
    "peritoneal": (
        "Peritoneal and retroperitoneal spaces:\n"
        "No peritoneal or retroperitoneal effusion or hyperechogenic fat is evident."
    ),
}

TEMPLATE_REGIONS = {"abdomen": ABDOMEN_PARTS}

OMIT_ALIASES = {
    "hepatobiliary": "abdomen.hepatobiliary",
    "liver": "abdomen.hepatobiliary",
    "hepatic": "abdomen.hepatobiliary",
    "gallbladder": "abdomen.hepatobiliary",
    "biliary": "abdomen.hepatobiliary",
    "porta hepatis": "abdomen.hepatobiliary",
    "spleen": "abdomen.spleen",
    "splenic": "abdomen.spleen",
    "pancreas": "abdomen.pancreas",
    "pancreatic": "abdomen.pancreas",
    "gastrointestinal": "abdomen.gastrointestinal",
    "gi": "abdomen.gastrointestinal",
    "stomach": "abdomen.gastrointestinal",
    "intestine": "abdomen.gastrointestinal",
    "intestines": "abdomen.gastrointestinal",
    "duodenum": "abdomen.gastrointestinal",
    "jejunum": "abdomen.gastrointestinal",
    "ileum": "abdomen.gastrointestinal",
    "colon": "abdomen.gastrointestinal",
    "urogenital": "abdomen.urogenital",
    "kidney": "abdomen.urogenital",
    "kidneys": "abdomen.urogenital",
    "renal": "abdomen.urogenital",
    "bladder": "abdomen.urogenital",
    "urinary bladder": "abdomen.urogenital",
    "adrenals": "abdomen.adrenals",
    "adrenal": "abdomen.adrenals",
    "adrenal glands": "abdomen.adrenals",
    "lymph_nodes": "abdomen.lymph_nodes",
    "lymph nodes": "abdomen.lymph_nodes",
    "jejunal lymph nodes": "abdomen.lymph_nodes",
    "peritoneal": "abdomen.peritoneal",
    "retroperitoneal": "abdomen.peritoneal",
    "effusion": "abdomen.peritoneal",
}

TEMPLATE_PART_GUIDE = """\
- abdomen.hepatobiliary: liver, gallbladder, biliary tree, porta hepatis
- abdomen.spleen: spleen / splenic parenchyma / splenic vessels
- abdomen.pancreas: pancreas
- abdomen.gastrointestinal: stomach, intestines, colon, GI tract
- abdomen.urogenital: kidneys, urinary bladder
- abdomen.adrenals: adrenal glands
- abdomen.lymph_nodes: jejunal, colic, and medial iliac lymph nodes
- abdomen.peritoneal: peritoneal / retroperitoneal spaces, abdominal effusion
"""


def valid_omit_keys() -> set[str]:
    return valid_keys_from_regions(TEMPLATE_REGIONS)


def assemble_templates(omit: set[str]) -> dict[str, str]:
    return assemble_region_blocks(TEMPLATE_REGIONS, omit)


REPORT_TASK = (
    "Format the provided professional clinical text into an Abdominal Ultrasound (US) report with Findings and "
    "Conclusion. When the literal phrase normal abdomen appears, apply the (already pruned) institutional template "
    "for remaining normal organs, then list each abnormal organ separately with bullets. Substitute measurements "
    "from dictation for every [X] slot when values are stated."
)

_OMIT_HEADINGS = {
    "abdomen.hepatobiliary": "Hepatobiliary system",
    "abdomen.spleen": "Spleen",
    "abdomen.pancreas": "Pancreas",
    "abdomen.gastrointestinal": "Gastrointestinal tract",
    "abdomen.urogenital": "Urogenital system",
    "abdomen.adrenals": "Adrenal glands",
    "abdomen.lymph_nodes": "Lymph nodes",
    "abdomen.peritoneal": "Peritoneal and retroperitoneal spaces",
}


def get_report_rules(region_blocks: dict[str, str], omitted_keys: set[str]) -> str:
    abdomen_block = (region_blocks.get("abdomen") or "").strip()
    omitted = format_omitted_keys(omitted_keys)
    omit_headings = ", ".join(
        f"{key} → **{_OMIT_HEADINGS[key]}:**"
        for key in sorted(omitted_keys)
        if key in _OMIT_HEADINGS
    ) or "none"

    if abdomen_block:
        template_rule = f"""\
2. **normal abdomen** TEMPLATE (institution wording; already pruned)
   - Paste the institutional block in rule 4. Abnormal organs were already removed from it. Do not add them back
     as normal canned text.
   - Omitted (abnormal) parts: {omitted}

3. **[X] MEASUREMENT SUBSTITUTION (ultrasound normal abdomen template)**
   - Whenever **source** lists measurements (especially after phrases such as "normal abdomen with the following
     measurements", or any explicit listing of duodenum, jejunum, ileum, colon, kidneys, adrenals, lymph nodes, etc.),
     replace each **[X]** in the template with the dictated numeric value and unit (mm or cm) that matches that
     structure. Preserve mm vs cm as dictated.
   - Map values to **[X]** slots in anatomical order (e.g. first duodenum value → first intestinal [X] in the GI line).
   - If **source** does not supply a value for a given **[X]**, replace that **[X]** only with: **not specified in dictation**
     (never invent numbers). Skip [X] slots that belong to omitted organs (they will not appear in the block).

4. Institutional **normal abdomen** block (normal organs only). Paste EXACTLY the following (including blank lines),
   with every **[X]** substituted per rule 3. Do not add/remove remaining sentences:
{abdomen_block}
"""
        findings_rule = f"""\
5. FINDINGS layout — the template IS being used. Follow this order exactly:
   a) **Findings** on its own line, then one blank line.
   b) **Abdominal US:** on its own line, then one blank line.
   c) The pruned canned block from rule 4 (remaining normal organs, institutional wording).
   d) Then EVERY omitted/abnormal organ from **source**. Do not skip (d) when omitted parts is not none.
      Heading map: {omit_headings}
      Each abnormal organ: heading ending with a colon, then ONLY bullet lines prefixed with "• ".
      One blank line between the canned block and the first abnormal heading, and between abnormal organ blocks.
      Do not use canned normal sentences for these organs.

   Target shape (example: spleen abnormal, other canned organs kept):

   Findings

   Abdominal US:

   Hepatobiliary system:
   <canned normal hepatobiliary paragraph>

   Pancreas:
   <canned normal pancreas paragraph>

   Spleen:
   • <abnormal findings from source>
"""
    else:
        template_rule = f"""\
2. **normal abdomen** TEMPLATE
   - Do NOT insert the institutional normal-abdomen block (the cue was absent, or every organ part was omitted as
     abnormal). Write Findings only from **source**.
   - Omitted (abnormal) parts: {omitted}

3. **[X] MEASUREMENT SUBSTITUTION**
   - Not applicable to an institutional template (none is inserted). Do not invent measurements.

4. Institutional **normal abdomen** Findings block: do not include one.
"""
        findings_rule = """\
5. FINDINGS layout — no institutional template. Follow this order exactly:
   a) **Findings** on its own line, then one blank line.
   b) **Abdominal US:** on its own line, then one blank line.
   c) Organ/system subheadings ending with a colon, each followed ONLY by bullet lines prefixed with "• ".
   d) Include blocks ONLY for systems explicitly mentioned in **source**. Do NOT add filler for unmentioned organs.
   e) Leave one blank line between organ/system blocks.
"""

    return f"""\
OUTPUT RULES (must follow exactly):

Let **source** mean the provided professional clinical text.
Let **cues** mean the text inside the XML tag <dictation_template_cues> in the same input (may be empty). Each
non-empty line of **cues** is a canonical cue from the raw transcript (e.g. a line exactly `normal abdomen`).

1. Use ONLY these two sections: **Findings** and **Conclusion**.

{template_rule}
{findings_rule}
6. CONCLUSION (always output after Findings)
   Conclusion
   1. <Summary of the primary abnormality>. <Clinical interpretation or prioritized differential diagnoses>.
   2. <Summary of a secondary abnormality or incidental finding>. <Interpretation of the finding>.
   3. <Summary of remaining observations, often noting a lack of metastasis or normal general status>.

   Ground each line in **source**; if the study is entirely normal and **source** says so, write concise normal
   summaries without inventing pathology.

7. Do not output bracket placeholders like "[Organ System...]" except the measurement substitution process for [X]
   in rule 3 (final output must contain no raw "[X]" tokens).
8. Keep content specific and anatomical. Do not add extraneous sections (e.g., history, technique).
9. Ensure to use Oxford comma to separate any continuous adjectives in a sentence.
"""
