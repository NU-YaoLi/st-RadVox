"""Prompts for CT-style radiology report generation (professional clinical + structured report)."""

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
"""

REPORT_TASK = "Format the provided professional clinical text into a structured CT Radiology Report."

REPORT_RULES = """\
OUTPUT RULES (must follow exactly):
1. Focus ONLY on two sections: "Diagnostic Interpretation" and "Conclusions". Omit all other parts.
2. Infer the major body regions being discussed from the text (CT is whole-body; prefer broad regions).
   Examples: Head/Neck, Thorax, Abdomen, Pelvis/Urogenital, Musculoskeletal/Spine, Lymph nodes, Other.
3. Categorize the findings under these body regions. If a region has no relevant findings, omit it.
4. Use exactly this structure (including headings, colons, bullets, and blank lines). Do NOT include placeholder text like "<Body Part 1>" in the output:

Diagnostic Interpretation
<Body Region 1>: <Paragraph description of findings>
<Body Region 2>: <Paragraph description of findings>
<Additional regions as needed>: <Paragraph description of findings>

Conclusions
<Body Region 1>:
• <Bullet point 1>
• <Bullet point 2>
<Body Region 2>:
• <Bullet point 1>
<Additional regions as needed>:
• <Bullets...>

5. Formatting requirements:
   - Each region header MUST end with a colon, e.g., "Thorax:", "Abdomen:".
   - In "Diagnostic Interpretation", use ONE paragraph per region (no bullet points there).
   - In "Conclusions", use ONLY bullet points prefixed with "• " under each region (no paragraphs there).
   - Leave exactly one blank line between region blocks and between the two main sections.
6. Keep content specific and anatomical. Do not add extraneous sections (e.g., history, technique).
7. Ensure to use Oxford comma to separate any continuous adjectives in a sentence.
"""
