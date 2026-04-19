"""Prompts for abdominal ultrasound (US) report generation."""

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

REPORT_TASK = "Format the provided professional clinical text into an Abdominal Ultrasound (US) report."

REPORT_RULES = """\
OUTPUT RULES (must follow exactly):
1. Use ONLY these two sections: "Findings" and "Conclusion".
2. The report MUST exactly follow this structure (including headings, colons, bullets, and blank lines). Do NOT include bracket placeholders like "[Organ System...]".

Findings
Abdominal US:
<Organ System/Body Part 1>:
• <bullet describing specific anatomical details, such as size, shape, margins, and echogenicity>
• <optional additional bullet for further observations within the same system>

<Organ System/Body Part 2>:
• <bullet describing specific anatomical details>

<Additional Organ Systems as needed...>:
• <bullets...>

Conclusion
1. <Summary of the primary abnormality>. <Clinical interpretation or prioritized differential diagnoses>.
2. <Summary of a secondary abnormality or incidental finding>. <Interpretation of the finding>.
3. <Summary of remaining observations, often noting a lack of metastasis or normal general status>.

3. Findings formatting requirements:
   - Each organ/system heading MUST end with a colon, e.g., "GIT:", "Pancreas:", "Spleen:".
   - Under each heading, output ONLY bullet points prefixed by "• " (bullets-only; no paragraphs).
   - Include organ/system blocks ONLY for organs/systems explicitly mentioned in the provided text. Do NOT add “expected” organs.
   - Do NOT output placeholder or filler blocks for unmentioned organs (e.g., do not write "Kidneys:" then "• Not reliably assessed.").
   - If an organ/system IS mentioned but not evaluated or is limited, you may state that limitation ONLY if the text indicates it.
   - For any mentioned organ/system, include at least one bullet; if normal, state it as a bullet (e.g., "• Unremarkable.").
   - Leave exactly one blank line between organ/system blocks.
4. Keep content specific and anatomical. Do not add extraneous sections (e.g., history, technique).
5. Ensure to use Oxford comma to separate any continuous adjectives in a sentence.
"""
