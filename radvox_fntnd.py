# pip3 install streamlit openai
# brew install ffmpeg

# Open Terminal: Press Command + Space, type Terminal, and hit Enter.
# Check for Homebrew: Type brew -v and hit Enter.
# If it shows a version number, skip to Step 3.
# If it says "command not found," paste this and hit Enter:
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# brew install ffmpeg

# Verify: Once finished, type ffmpeg -version. If you see FFmpeg version 8.1 "Hoare" (the March 2026 release) or similar, you are good to go!

# pkill -f streamlit
# streamlit run voxrad_fntnd.py
# Note: Since this uses browser-based recording, you do not need to install OS-level audio dependencies.

import streamlit as st
import tempfile
import os
import subprocess
from datetime import datetime

# Import the refactored processing function from the backend
from radvox_bknd import process_audio

# --- Configuration & Setup ---
st.set_page_config(page_title="RadVox: Vet Radiology Voice Assistant", layout="centered")

st.markdown(
    """
    <style>
    /* Hide multipage navigation (left menu) */
    [data-testid="stSidebarNav"] { display: none; }

    /* Target the main content container */
    [data-testid="stMainBlockContainer"] {
        max-width: 1200px !important;
        padding-top: 2rem;
    }

    .stText {
        white-space: pre-wrap !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Fetch API Key from Streamlit Secrets
try:
    API_KEY = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("⚠️ OPENAI_API_KEY is not set in Streamlit secrets.")
    st.stop()

# Initialize session state variables
if "audio_key" not in st.session_state:
    st.session_state.audio_key = 0
if "audio_chunks" not in st.session_state:
    st.session_state.audio_chunks = []
if "last_recorded_bytes" not in st.session_state:
    st.session_state.last_recorded_bytes = None
if "last_audio" not in st.session_state:
    st.session_state.last_audio = None
if "transcription" not in st.session_state:
    st.session_state.transcription = ""
if "pro_version" not in st.session_state:
    st.session_state.pro_version = ""
if "report_version" not in st.session_state:
    st.session_state.report_version = ""
if "history" not in st.session_state:
    st.session_state.history = []

# --- Helper Functions ---
def _ffmpeg_concat_escape_path(path: str) -> str:
    # ffmpeg concat demuxer list file expects forward slashes and single-quote escaping
    return path.replace("\\", "/").replace("'", r"'\''")

def stitch_audio_chunks(chunks):
    """Concatenates multiple audio byte chunks into a single WAV file using subprocess."""
    with tempfile.TemporaryDirectory() as tmpdir:
        list_file_path = os.path.join(tmpdir, "list.txt")
        
        # Write chunks to disk and prepare ffmpeg list file
        with open(list_file_path, "w", encoding="utf-8", newline="\n") as list_file:
            for i, chunk in enumerate(chunks):
                chunk_path = os.path.join(tmpdir, f"chunk_{i}.wav")
                with open(chunk_path, "wb") as f:
                    f.write(chunk)
                list_file.write(f"file '{_ffmpeg_concat_escape_path(chunk_path)}'\n")

        output_path = os.path.join(tmpdir, "output.wav")
        
        # Run native subprocess concatenation
        subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-nostdin",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                list_file_path,
                "-c",
                "copy",
                output_path,
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        with open(output_path, "rb") as f:
            return f.read()

def _go_to_surprise_page() -> None:
    # Streamlit's switch_page path expectations vary across versions/setups.
    for target in ("pages/radvox_fntnd_sp.py", "radvox_fntnd_sp.py"):
        try:
            st.switch_page(target)
            return
        except Exception:
            continue
    st.error("Couldn't navigate to the Surprise page. Make sure `pages/radvox_fntnd_sp.py` exists.")

# --- Sidebar: History ---
if st.sidebar.button("surprise", use_container_width=True):
    _go_to_surprise_page()

st.sidebar.title("📚 Conversion History")
if not st.session_state.history:
    st.sidebar.info("No saved records yet. Transcribe and save audio to see history here.")
else:
    # Display history in reverse order (newest first)
    for i, record in enumerate(reversed(st.session_state.history)):
        with st.sidebar.expander(f"Record: {record['timestamp']}"):
            st.write("**Original Transcript:**")    
            st.text(record["original"]) # using st.text preserves \n visually better than st.write
            st.write(f"**Saved Version ({record['choice']}):**")
            st.text(record["saved_text"])

# --- Main App UI ---
# Top Section layout with Title on left and Model/Report selectors on right
title_col, toggle_col = st.columns([3, 1])

with title_col:
    st.title("🎙️ Vet Radiology Voice Assistant")
    st.write("Record your radiology notes below to generate transcribed, professional clinical, and radiology report versions.")

with toggle_col:
    # Add some padding to push it down slightly so it aligns nicely with the title
    st.write("\n") 
    selected_model = st.radio(
        "Transcription Model:",
        ("gpt-4o-transcribe", "whisper-1"),
        index=0
    )
    report_type = st.radio(
        "Report Type:",
        ("CT", "US"),
        index=0,
    )

# Audio Recorder Widget
st.write("\n") 
st.write("### 1. Record Audio (You can record multiple parts)")

# Give the widget a dynamic key so we can force it to reset
new_audio = st.audio_input(
    "Dictate your notes here:", 
    key=f"audio_input_{st.session_state.audio_key}"
)

# If new audio is recorded, append it to our chunks list
if new_audio and new_audio.getvalue() != st.session_state.last_recorded_bytes:
    st.session_state.last_recorded_bytes = new_audio.getvalue()
    st.session_state.audio_chunks.append(new_audio.getvalue())
    st.rerun() # Refresh to show updated chunk count

# Display how many clips have been recorded
if st.session_state.audio_chunks:
    st.success(f"🎙️ {len(st.session_state.audio_chunks)} audio segment(s) recorded.")
    
    col_proc, col_clear = st.columns(2)
    with col_proc:
        process_clicked = st.button("Process Full Dictation", type="primary", use_container_width=True)
    with col_clear:
        if st.button("Clear Recordings & Start Over", use_container_width=True):
            # 1. Clear the audio chunks and reset tracking
            st.session_state.audio_chunks = []
            st.session_state.last_recorded_bytes = None
            
            # 2. INCREMENT THE KEY to destroy the old widget and its ghost file
            st.session_state.audio_key += 1 
            
            # 3. CLEAR THE UI RESULTS BELOW
            st.session_state.last_audio = None
            st.session_state.transcription = ""
            st.session_state.pro_version = ""
            st.session_state.report_version = ""
            
            st.rerun()

    if process_clicked:
        if not API_KEY or "sk-sk" in API_KEY:
            st.warning("⚠️ The provided API key is invalid or incomplete.")
            
        with st.spinner(f"Combining audio natively, transcribing with {selected_model}, and processing notes..."):
            try:
                # Stitch the audio chunks together using native subprocess helper
                final_audio_bytes = stitch_audio_chunks(st.session_state.audio_chunks)

                # Pass the combined audio to the backend module
                transcription, pro_version, report_version = process_audio(
                    API_KEY,
                    final_audio_bytes,
                    selected_model,
                    report_type,
                )
                
                # Save all results to session state
                st.session_state.last_audio = final_audio_bytes
                st.session_state.transcription = transcription
                st.session_state.pro_version = pro_version
                st.session_state.report_version = report_version
                
            except Exception as e:
                st.error(f"An API or system error occurred.\n\nError details: {e}")

# Display Results and Save Options
if st.session_state.transcription:
    st.write("\n")
    st.write("---")
    st.write("### 2. Original Transcription")
    # Using st.text to ensure newlines render accurately on screen
    st.text(st.session_state.transcription)
    
    st.write("\n")
    st.write("---")
    st.write("### 3. Polished Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Professional Clinical Version")
        st.text(st.session_state.pro_version)
        
    with col2:
        st.subheader("Radiology Report Version")
        st.text(st.session_state.report_version) 

    st.write("\n")
    st.write("---")
    st.write("### 4. Save to History")
    
    # Selection mechanism for saving
    save_choice = st.radio(
        "Which version would you like to save to your history?",
        ("Professional Clinical Version", "Radiology Report Version"),
        horizontal=True
    )
    
    if st.button("Save Selected Version"):
        # Determine which text to save based on the radio button choice
        text_to_save = st.session_state.pro_version if save_choice == "Professional Clinical Version" else st.session_state.report_version
        
        # Append to the history list
        st.session_state.history.append({
            "timestamp": datetime.now().strftime("%I:%M %p"),
            "original": st.session_state.transcription,
            "choice": save_choice,
            "saved_text": text_to_save
        })
        
        st.toast("Saved successfully! Check the sidebar.")
        st.rerun()