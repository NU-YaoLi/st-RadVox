# RadVox: Vet Radiology Voice Assistant

RadVox is a browser dictation tool for veterinary radiologists. Speak findings in the mic, and the app returns a transcript, a polished clinical narrative, and a structured report ready to paste into a PDF form.

**App:** [https://radvox.streamlit.app/](https://radvox.streamlit.app/)

The app is **deployed on Streamlit Community Cloud**. Open it in Chrome or Edge, allow the microphone, and dictate. There is nothing to install and no local terminal command.

Source: [NU-YaoLi/st-RadVox](https://github.com/NU-YaoLi/st-RadVox)

---

## Who it is for

Veterinary radiologists, clinicians, and clinic staff who want consistent, institution-style reports without retyping canned normal language or fighting PDF formatting.

---

## What you get from one dictation

After **Process Full Dictation**, RadVox shows three texts:

1. **Original transcription** — what the speech model heard, with spoken “next line” turned into real line breaks.
2. **Professional clinical version** — a doctor-to-doctor polish of that dictation (newlines kept; stacked adjectives get Oxford commas).
3. **Radiology report version** — a structured, **plain-text** report (no bullets, numbering, or markdown) so it pastes cleanly into a PDF. Layout depends on the report type you picked in the sidebar.

Save either polished version to **History** (sidebar). History lives in this browser tab’s session only; it is not a clinic archive and it disappears if you close the tab or the session expires.

---

## How to dictate a study

1. In the sidebar, choose **Report type** (CT, US, Radiograph, or MRI) and **Recording mode** (Quick or Regular).
2. Record one or more clips in the browser. You do not need extra audio software.
3. Click **Process Full Dictation**.
4. Review the three outputs. Save the version you want to History if you need it later in this sitting.
5. Dictate the next case in the same tab. After a **successful** process, RadVox **releases the WAV clips** from the session so they are not mixed into the next report and do not keep filling memory. The text of the last report stays on screen until you process again or click **Clear Recordings & Start Over**.

Spoken formatting cue: say **“next line”** when you want a line break in the transcript.

---

## Recording modes

| Mode | Behavior |
|---|---|
| **Quick** | Each take is added as soon as you stop. Use this for a fast multi-clip dictation. |
| **Regular** | The latest take is staged until you click **Add clip**. Record again to replace a take you have not added yet. |

Both modes support several clips per study. Use **Clear Recordings & Start Over** if you want to throw away the current clips and the on-screen text.

If the mic widget shows *An error has occurred, please try again*, that clip did not upload (network, a very long take, or a browser glitch). Record that take again. It is not an OpenAI “overuse” message.

---

## Report types and templates

Pick the modality that matches the study **before** you process. Unknown types fall back to CT.

| Sidebar | Report shape | Literal spoken cues that insert canned normals |
|---|---|---|
| **CT** | Diagnostic Interpretation + Conclusions | `normal thorax`, `normal abdomen` |
| **US** | Findings + Conclusion (abdominal US) | `normal abdomen` |
| **Radiograph** | Findings + Conclusion | `normal thorax`, `normal abdomen` |
| **MRI** | Findings + Conclusion | `normal brain`, `normal spine` |

Cues must be the two-word phrase (for example “normal abdomen”), not a paraphrase such as “the abdomen is unremarkable.” If the dictation includes a cue **and** some organs are abnormal, RadVox keeps the institutional wording for the remaining normal parts and writes the abnormal organs from your dictation instead of the canned normal sentences.

Ultrasound and CT abdomen templates include `[X]` measurement slots. Dictated numbers are filled in; if a value was not spoken, the report uses `not specified in dictation` rather than inventing a number.

Conclusions are a flat impression list (most significant first). They are not numbered and are not grouped under body-region headers.

---

## Sidebar

- **Report type** and **recording mode** — used for the next process.
- **Transcription model** — from `bknd/radvox_bknd_params.py` (shown in the sidebar).
- **History** — saved texts from this session.
- **Surprise** — extra page in the app (not part of reporting).

---

## Practical notes

- Prefer a short, clear dictation over one very long take. Several clips in Quick mode is normal.
- Grant microphone permission when the browser asks. Chrome or Edge is more reliable than some privacy-hardened browsers.
- Reports are generated as plain text on purpose (PDF paste).
- Do not put secrets in the repo. The deployed app reads `OPENAI_API_KEY` from **Streamlit Cloud secrets**.

---

## Project layout (maintainers)

The live app’s entry point on Streamlit Cloud is `fntnd/radvox_fntnd.py`.

| Path | Role |
|---|---|
| `fntnd/` | Streamlit UI, sidebar, History, recorder session handling |
| `bknd/` | Transcription, clinical polish, template prune, report generation |
| `bknd/radvox_bknd_params.py` | Chat and transcription model IDs (change versions here) |
| `.streamlit/config.toml` | Cloud-oriented server limits (upload size, no file watcher) |
| `requirements.txt` | `streamlit` and `openai` |
