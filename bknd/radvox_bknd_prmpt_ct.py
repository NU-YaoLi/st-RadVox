"""CT prompts — clinic templates for literal normal thorax / normal abdomen + structured report."""

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

# Institutional CT paragraphs (verbatim wording) — trigger only on literal "normal thorax" / "normal abdomen".
_CT_NORMAL_THORAX = """\
Minimal, unstructured ground glass attenuation is noted in the dependent aspect of the pulmonary parenchyma, without nodules or masses. The airways are normal, without wall thickness or luminal collapse.

The cardiac chambers are normal, without dilation or an overt impression of wall thickening or thinning. The pulmonary vessels and great vessels are appropriate in size and morphology, without congestion.

The mediastinal and pleural spaces are within normal limits, without lymphadenopathy, mass lesions, or effusion. An incidental thymic remnant is noted in the cranioventral mediastinum.

The collimated cranial abdomen is normal, without nodules or mass lesions, lymphadenopathy, or effusion.

The osseous structures and external soft tissues are unremarkable.
"""

_CT_NORMAL_ABDOMEN = """\
The hepatic parenchyma is normal in attenuation and contrast enhancement, without nodules or masses. The gallbladder is normal in shape and size, with a small amount of incidental, hyperattenuating sludge. No biliary dilation is appreciated. The hepatic and portal vasculature is normal. At the porta hepatis, the hepatic lymph nodes are normal in size and appearance, measuring [X] mm.

The splenic parenchyma is normal in attenuation and contrast enhancement, without nodules or masses. The associated vasculature and lymph node are within normal limits.

The pancreatic parenchyma is normal in attenuation and contrast enhancement, without thickening or surrounding fat standing. The pancreaticoduodenal lymph node is small and normal.

The gastrointestinal tract is normal, with a small amount of luminal content noted in the stomach, without gastric wall thickening. Normal pyloric duodenal junction. Normal small intestines without an impression of generalized or regional wall thickening or architectural alteration. Normal ileocolic junction and large intestines. The jejunal and colic lymph nodes are appropriate, measuring [X] mm.

Bilaterally, the kidneys are normal and symmetrical in shape, size, margination, attenuation, and enhancement. No ureteral dilation is noted. The urinary bladder is normal, containing homogeneous urine, and without wall thickening or irregularity.

The adrenal glands are within normal limits, measuring [X] mm at the caudal pole on the left and [X] mm on the right.

No peritoneal or retroperitoneal effusion or fat stranding is evident.

The collimated caudal thorax is within normal limits.

The osseous structures and external soft tissues are unremarkable.
"""

REPORT_TASK = (
    "Format the provided professional clinical text into a structured CT Radiology Report using "
    "Diagnostic Interpretation and Conclusions. Apply institutional normal thorax/abdomen template paragraphs when "
    "triggers in the rules fire (including dictation_template_cues from raw transcript); replace every [X] in the "
    "abdomen template using numerals dictated in the professional clinical text when provided."
)

REPORT_RULES = f"""\
OUTPUT RULES (must follow exactly):

Let **source** mean the provided professional clinical text.
Let **cues** mean the text inside the XML tag <dictation_template_cues> in the same input (may be empty). Each
non-empty line of **cues** is a canonical cue detected from the raw transcript (e.g. a line exactly `normal thorax`).

1. Use ONLY these two sections, in this order: **Diagnostic Interpretation** and **Conclusions**.

2. TEMPLATE TRIGGERS (CT) — **professional_clinical_text** and/or **dictation_template_cues**
   - **normal thorax** template: apply if (a) **source** contains the case-insensitive substring **normal thorax**
     (word "normal", ASCII space, word "thorax"), OR (b) **cues** contains its own line exactly `normal thorax`.
     Do not use synonyms or paraphrases alone. If **source** clearly contradicts a globally normal thorax, do not
     apply the normal thorax template.
   - **normal abdomen** template (with [X] handling in rule 4): apply if (a) **source** contains the substring
     **normal abdomen**, OR (b) **cues** contains its own line exactly `normal abdomen`. If **source** clearly
     contradicts a globally normal abdomen, do not apply the normal abdomen template.
   - If **source** describes true abnormalities in a region, describe them accurately; do not replace abnormal
     narrative with a normal template for that region.

3. When rule 2 inserts the **normal thorax** block, under Diagnostic Interpretation output **Thorax:** on its own line,
   then a blank line, then paste EXACTLY the following institutional paragraph block (including blank lines).
   Do not add/remove sentences:
{_CT_NORMAL_THORAX.strip()}

4. When rule 2 inserts the **normal abdomen** block, you MUST output a single **Abdomen:** subsection (heading on its
   own line, then a blank line, then the paragraph), using the institutional text below, except that every token
   **[X]** must be replaced as follows:
   - If **source** states an explicit measurement for that slot (e.g. hepatic lymph nodes 5 mm, adrenal left 4 mm),
     substitute the dictated number and unit (mm or cm) for that **[X]**.
   - If **source** lists structured measurements (e.g. after "normal abdomen with the following measurements"),
     map each dictated value into the anatomically matching **[X]** in the template when unambiguous.
   - If a value for a given **[X]** was not dictated, replace only that **[X]** with: **not specified in dictation**
     (do not invent numbers).

   Then paste EXACTLY the following institutional paragraph block, with every **[X]** substituted per the rules above:
{_CT_NORMAL_ABDOMEN.strip()}

   If both **normal thorax** and **normal abdomen** triggers from rule 2 apply, output **Thorax:** block first, then
   **Abdomen:** block, separated by one blank line.

5. DIAGNOSTIC INTERPRETATION — structure
   - Output the heading **Diagnostic Interpretation** on its own line, then one blank line.
   - Immediately after that, in order: optional **Thorax:** template block (rule 3), optional **Abdomen:** template
     block (rule 4), then any additional body-region subsections from **source** (each header ending with a colon,
     followed by ONE paragraph; no bullets in this section).
   - If neither trigger from rule 2 applies, write Diagnostic Interpretation only from **source** using the same
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
