# RadVox: Vet Radiology Voice Assistant

A specialized Streamlit web application designed for veterinary radiologists to dictate clinical notes. The app records audio directly from the browser, transcribes it using OpenAI's audio models, and processes the text to generate both a grammar-corrected version and a highly polished, professional clinical version.

## ✨ Features

* **In-Browser Audio Recording:** Record multiple dictation segments directly within the web interface without needing third-party recording software.
* **High-Quality Transcription:** Utilizes OpenAI's state-of-the-art models (`gpt-4o-transcribe` or `whisper-1`) to convert spoken word to text.
* **AI-Powered Polishing:** Automatically generates two rewritten versions of the transcript:
  1. **Grammar Corrected Version:** Fixes basic spelling and verbal hiccups while maintaining the exact original phrasing.
  2. **Professional Clinical Version:** Rephrases the text into a formal clinical tone suitable for official records, ensuring all adjectives are properly separated by commas.
* **History Tracking:** Save your preferred versions to a session history sidebar for easy reference and copying.