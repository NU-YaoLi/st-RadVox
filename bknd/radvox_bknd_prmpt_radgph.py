"""Prompts for plain radiograph (survey radiography) — clinic normal paragraphs from templates.docx (Radiographs)."""

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

# Verbatim from templates.docx — Radiographs section (normal thorax / normal abdomen).
_NORMAL_THORAX_RADGRAPH = (
    "The pulmonary parenchyma is within normal limits, without nodules, masses, regions of consolidation, "
    "or abnormal lung patterns. The cardiac silhouette is normal, without generalized or specific chamber enlargement. "
    "The pulmonary vessels and great vessels are appropriate in size and morphology, without congestion. "
    "The mediastinal and pleural spaces are within normal limits. Mild, dynamic caudal esophageal fluid is noted "
    "on the left lateral view, consistent with incidental passive reflux. The collimated cranial abdomen is normal, "
    "with preserved serosal detail. The osseous structures and external soft tissues are unremarkable."
)

_NORMAL_ABDOMEN_RADGRAPH = (
    "The stomach is normal in size, containing mild, unstructured, heterogeneous, fluid and gas content, which "
    "exhibits appropriate redistribution into the pylorus on the left lateral view, suggesting patency at the time "
    "of imaging. The small intestines consist of a homogeneous population, without dilation or plication. "
    "The large intestines are within normal limits, containing gas and heterogeneous, formed fecal content. "
    "The visible hepatic, splenic, renal, and urinary bladder silhouettes are within normal limits for shape, size, "
    "margination, and opacity. The serosal detail of the peritoneal and retroperitoneal spaces is preserved. "
    "The collimated caudal thorax is unremarkable. The osseous structures and external soft tissues are unremarkable."
)

REPORT_TASK = (
    "Format the provided professional clinical text into a structured plain radiograph report. "
    "Use Findings plus Conclusion (singular). Apply institutional normal thorax/abdomen paragraphs only when the "
    "source text contains the literal phrases specified in the rules (case-insensitive substring match)."
)

REPORT_RULES = f"""\
OUTPUT RULES (must follow exactly):

1. Use ONLY these two sections: "Findings" and "Conclusion".

2. The report MUST follow the structure below (headings, colons, blank lines). Do NOT include bracket placeholders
   like "[Organ System...]" in the output.

3. TEMPLATE TRIGGERS (Radiographs) — **professional_clinical_text** and/or **dictation_template_cues**
   - Let **source** mean the provided professional clinical text.
   - Let **cues** mean the text inside the XML tag <dictation_template_cues> in the same input (may be empty). Each
     non-empty line of **cues** is a canonical cue from the raw transcript (e.g. `normal thorax`).
   - Use the standard **thorax** paragraph in Findings if (a) **source** contains the case-insensitive substring
     **normal thorax**, OR (b) **cues** contains its own line exactly `normal thorax`. Do NOT use this paragraph
     based on synonyms or paraphrases alone. If **source** clearly contradicts a globally normal thorax, do not apply
     the template.
   - Use the standard **abdomen** paragraph in Findings if (a) **source** contains the substring **normal abdomen**,
     OR (b) **cues** contains its own line exactly `normal abdomen`. Do not apply if **source** clearly contradicts
     a globally normal abdomen.
   - If **source** describes real abnormalities in a region, describe them accurately; do not replace abnormal
     narrative with a normal template paragraph for that region.
   - When the thorax rule fires, under Findings output a subsection: a line **Thorax:** then a blank line, then this
     paragraph copied **verbatim** (same wording and sentence order, no summarizing):

   {_NORMAL_THORAX_RADGRAPH}

   - When the abdomen rule fires, under Findings output a subsection: a line **Abdomen:** then a blank line, then this
     paragraph copied **verbatim**:

   {_NORMAL_ABDOMEN_RADGRAPH}

   - If both literals appear, output **Thorax:** block first, then **Abdomen:** block, each separated by one blank line.

4. FINDINGS — remainder of the section
   - Begin Findings with the heading **Findings** on its own line, then a blank line.
   - After any Thorax:/Abdomen: template blocks from rule 3, add other regions, projections, or abnormalities from
     **source** using subheadings that MUST end with a colon (e.g., "Musculoskeletal:", "Additional:").
   - Under each such subheading (other than the verbatim template paragraphs above), use ONLY bullet points prefixed
     by "• " (bullets-only; no paragraphs under those headings).
   - If neither trigger from rule 3 applies, write Findings only from **source** using the same subheading + bullet
     conventions; do not invent the institutional normal paragraphs.
   - Include blocks ONLY for regions or topics explicitly mentioned in **source**. Do NOT add filler blocks for
     unmentioned regions.
   - Leave exactly one blank line between distinct subsections under Findings.

5. CONCLUSION (singular — same numbered convention as ultrasound reports)
   After one blank line following the Findings section, output the heading **Conclusion** then exactly:

   Conclusion
   1. <Summary of the primary abnormality>. <Clinical interpretation or prioritized differential diagnoses>.
   2. <Summary of a secondary abnormality or incidental finding>. <Interpretation of the finding>.
   3. <Summary of remaining observations, often noting a lack of metastasis or normal general status>.

   Use three numbered lines as shown; replace angle-bracket guidance with content grounded in **source**.

6. Keep content specific and anatomical. Do not add extraneous sections (e.g., history, technique).
7. Ensure to use Oxford comma to separate any continuous adjectives in a sentence.
"""
