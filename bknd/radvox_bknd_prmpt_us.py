"""US prompts — clinic normal-abdomen template + standard abdominal US report."""

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

# Institutional normal-abdomen US template — [X] replaced from dictation per REPORT_RULES.
_US_NORMAL_ABDOMEN_BLOCK = """\
Hepatobiliary system:
The hepatic parenchyma is within normal limits for shape, size, echogenicity, and echotexture, without nodules or masses. Preserved portal markings. The gallbladder is normal, containing anechoic bile and a small amount of incidental, unstructured, echogenic sludge. No gallbladder wall thickening or biliary dilation is evident. At the porta hepatis, no lymphadenomegaly is noted, and the portal vessel is normal upon evaluation with spectral Doppler.

Spleen:
The splenic parenchyma is within normal limits for shape, size, echogenicity, and echotexture, without nodules or masses. Normal splenic vascularity is noted with color Doppler evaluation.

Pancreas:
The pancreas is normal in thickness and echogenicity, without surrounding hyperechogenicity.

Gastrointestinal tract:
The stomach is normal in size, containing a small amount of gas, causing a mild reverberation artifact, mildly limiting visualization of the dorsal wall. The visible aspects of the gastric walls and the pyloric duodenal junction are within normal limits. The small intestines are traced, with normal wall architecture and thicknesses noted:  duodenum [X] mm, jejunum [X] mm, and ileum [X] mm. The ileocolic junction and large intestines are normal, with colonic wall thickness of [X] mm.

Urogenital system:
Bilaterally, the kidneys are normal and symmetrical in shape, size, margination, and corticomedullary definition, measuring [X] cm in length on the left and [X] cm on the right. No renal pelvic dilation or perirenal hyperechogenicity is noted. The urinary bladder is normal, containing anechoic urine, and without wall thickening or irregularity.

Adrenal glands:
The adrenal glands are within normal limits, measuring [X] mm at the caudal pole on the left and [X] mm on the right.

Lymph nodes:
The jejunal and colic lymph nodes are normal, measuring [X] mm and [X] mm respectively. The medial iliac lymph nodes are symmetrical and normal, measuring [X] mm on the left and [X] mm on the right.

Peritoneal and retroperitoneal spaces:
No peritoneal or retroperitoneal effusion or hyperechogenic fat is evident.
"""

REPORT_TASK = (
    "Format the provided professional clinical text into an Abdominal Ultrasound (US) report with Findings and "
    "Conclusion. When the literal phrase normal abdomen appears, apply the institutional template and substitute "
    "measurements from dictation for every [X] slot when values are stated."
)

REPORT_RULES = f"""\
OUTPUT RULES (must follow exactly):

Let **source** mean the provided professional clinical text.
Let **cues** mean the text inside the XML tag <dictation_template_cues> in the same input (may be empty). Each
non-empty line of **cues** is a canonical cue from the raw transcript (e.g. a line exactly `normal abdomen`).

1. Use ONLY these two sections: **Findings** and **Conclusion**.

2. **normal abdomen** TEMPLATE (institution wording)
   - Apply the institutional block below if (a) **source** contains the case-insensitive substring **normal abdomen**
     (word "normal", space, word "abdomen"), OR (b) **cues** contains its own line exactly `normal abdomen`.
   - Do NOT use this block based on synonyms or paraphrases alone (without (a) or (b)).
   - If **source** describes true abdominal abnormalities, describe them accurately; you may follow the template
     only for organs explicitly stated as normal, and write abnormal findings separately under appropriate headings.

3. **[X] MEASUREMENT SUBSTITUTION (ultrasound normal abdomen template)**
   - Whenever **source** lists measurements (especially after phrases such as "normal abdomen with the following
     measurements", or any explicit listing of duodenum, jejunum, ileum, colon, kidneys, adrenals, lymph nodes, etc.),
     replace each **[X]** in the template with the dictated numeric value and unit (mm or cm) that matches that
     structure. Preserve mm vs cm as dictated.
   - Map values to **[X]** slots in anatomical order (e.g. first duodenum value → first intestinal [X] in the GI line).
   - If **source** does not supply a value for a given **[X]**, replace that **[X]** only with: **not specified in dictation**
     (never invent numbers).

4. Institutional **normal abdomen** Findings block (apply rules 2–3 only when rule 2 fires). When rule 2 fires,
   output exactly this placeholder token on its own line (the backend will insert the institutional template and
   substitute all **[X]** per rule 3):
   {{TEMPLATE_US_NORMAL_ABDOMEN}}
   When rule 2 does **not** fire, do **not** include this placeholder.

5. FINDINGS — when the **normal abdomen** trigger from rule 2 does NOT apply
   - Use the heading **Findings**, then **Abdominal US:**, then organ/system subheadings ending with a colon, each
     followed ONLY by bullet lines prefixed with "• " (same as prior RadVox US behavior).
   - Include blocks ONLY for systems explicitly mentioned in **source**. Do NOT add filler for unmentioned organs.
   - Leave one blank line between organ/system blocks.

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
