"""MRI prompts — clinic templates for literal normal brain / normal spine + structured report."""

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

_MRI_NORMAL_BRAIN = """\
The cerebral, midbrain, cerebellar, and brain stem structures are all within normal limits for signal intensity and structural symmetry, without abnormal contrast enhancement. No susceptibility artifact is noted on GRE images, and no restriction of diffusion is noted on DWI images. The ventricular system is normal, without dilation. The visible cranial nerves are normal and symmetrical. No midline shift or brain herniation is present.

The extra-cranial osseous structures and soft tissues are within normal limits, with normal and symmetrical mandibular and medial retropharyngeal lymph nodes.
"""

_MRI_NORMAL_SPINE = """\
The vertebral bodies, intervertebral disc spaces, articular process joints, and all remaining osseous structures and paravertebral soft tissues are within normal limits. The intervertebral discs demonstrate appropriate T2 hyperintensity, without evidence of degeneration, protrusion, or extrusion. No abnormal contrast enhancement is appreciated. 
"""

REPORT_TASK = (
    "Format the provided professional clinical text into an MRI report with Findings and Conclusion. "
    "Apply institutional normal brain / normal spine template paragraphs only when the literal triggers in the "
    "rules are present."
)

REPORT_RULES = f"""\
OUTPUT RULES (must follow exactly):

Let **source** mean the provided professional clinical text.
Let **cues** mean the text inside the XML tag <dictation_template_cues> in the same input (may be empty). Each
non-empty line of **cues** is a canonical cue from the raw transcript (e.g. `normal brain`).

1. Use ONLY these two sections: **Findings** and **Conclusion**.

2. TEMPLATE TRIGGERS (MRI) — **source** and/or **dictation_template_cues**
   - Insert the institutional **normal brain** paragraph if (a) **source** contains the case-insensitive substring
     **normal brain**, OR (b) **cues** contains its own line exactly `normal brain`. No synonyms or paraphrases alone.
   - Insert the institutional **normal spine** paragraph if (a) **source** contains the substring **normal spine**,
     OR (b) **cues** contains its own line exactly `normal spine`.
   - If **source** describes abnormalities in brain or spine, describe them accurately; do not replace abnormal
     narrative with a normal template for that region.

3. When the **normal brain** rule fires, under Findings output **Brain:** on its own line, a blank line, then this
   placeholder token on its own line (backend will paste the institutional paragraph with line breaks):
   {{TEMPLATE_MRI_NORMAL_BRAIN}}

4. When the **normal spine** rule fires, under Findings output **Spine:** on its own line, a blank line, then this
   placeholder token on its own line:
   {{TEMPLATE_MRI_NORMAL_SPINE}}

   If both literals appear, output **Brain:** first, then **Spine:**, separated by one blank line.

5. FINDINGS — structure
   - Heading **Findings** on its own line, then one blank line.
   - Then optional template blocks from rules 3–4 in order.
   - Then any additional MRI-related subsections from **source** (e.g., soft tissues, contrast phases) using headings
     ending with a colon, followed by ONLY bullet lines prefixed with "• " unless the template already used a
     paragraph block above.
   - If neither trigger from rule 2 applies, write Findings only from **source** with colon headings and bullets as above.
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
