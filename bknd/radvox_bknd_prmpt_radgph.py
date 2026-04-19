"""Prompts for plain radiograph reports — replace REPORT_* when you finalize modality-specific rules."""

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

REPORT_TASK = (
    "Format the provided professional clinical text into a structured plain radiograph (survey radiology) report."
)

# TODO: Replace with finalized radiograph-specific structure (views, skeletal regions, etc.).
REPORT_RULES = """\
OUTPUT RULES (must follow exactly):
1. Use ONLY these two sections: "Findings" and "Conclusions".
2. Organize findings by anatomic region or projection when the source text supports it (e.g., Thorax, Abdomen, Appendicular skeleton).
3. Use exactly this structure (including headings, colons, bullets, and blank lines). Do NOT include placeholder tokens like "<Region 1>" in the output:

Findings
<Region or projection 1>:
• <Concise bullet describing opacity, margination, alignment, or other radiographic features>

<Region or projection 2>:
• <Bullets as needed>

Conclusions
• <Primary interpretation or differential, tied to the findings>.
• <Secondary or incidental findings if any>.
• <Limitations only if explicitly stated in the source text>.

4. Formatting requirements:
   - Each subheading under Findings MUST end with a colon.
   - Under each heading, use ONLY bullet points prefixed by "• ".
   - Leave exactly one blank line between blocks under Findings and before Conclusions.
5. Keep content specific and anatomical. Do not add extraneous sections (e.g., full history, detailed technique) unless present in the source.
6. Ensure to use Oxford comma to separate any continuous adjectives in a sentence.
"""
