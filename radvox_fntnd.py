# pip3 install streamlit openai
# brew install ffmpeg
#
# Open Terminal: Press Command + Space, type Terminal, and hit Enter.
# Check for Homebrew: Type brew -v and hit Enter.
# If it shows a version number, skip to Step 3.
# If it says "command not found," paste this and hit Enter:
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# brew install ffmpeg
#
# Verify: Once finished, type ffmpeg -version. If you see FFmpeg version 8.1 "Hoare" (the March 2026 release) or similar, you are good to go!
#
# pkill -f streamlit
# streamlit run voxrad_fntnd.py
# Note: Since this uses browser-based recording, you do not need to install OS-level audio dependencies.
import hashlib
from datetime import datetime
import streamlit as st
from radvox_audio import stitch_audio_chunks
from radvox_bknd import process_audio
from radvox_sidebar import render_sidebar_nav_and_settings
from radvox_ui import inject_base_css
# --- Configuration & Setup ---
st.set_page_config(page_title="RadVox: Vet Radiology Voice Assistant", layout="centered")
inject_base_css(include_st_text_pre_wrap=True)
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
if "last_recorded_hash" not in st.session_state:
    st.session_state.last_recorded_hash = None
if "pending_audio_bytes" not in st.session_state:
    st.session_state.pending_audio_bytes = None
if "pending_audio_hash" not in st.session_state:
    st.session_state.pending_audio_hash = None
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
# Toast after save: st.rerun() right after st.toast() drops the toast; show on next run.
if st.session_state.pop("_show_save_toast", False):
    st.toast("Saved successfully! Open History in the sidebar to review.")
# --- Sidebar: navigation + application settings ---
selected_model, report_type, recording_mode = render_sidebar_nav_and_settings()
# --- Main App UI ---
st.title("🎙️ Vet Radiology Voice Assistant")
st.write("Record your radiology notes below to generate transcribed, professional clinical, and radiology report versions.")
# If user switched to Quick with a clip still staged, merge it like Add clip
if recording_mode == "Quick" and st.session_state.pending_audio_bytes:
    st.session_state.audio_chunks.append(st.session_state.pending_audio_bytes)
    st.session_state.last_recorded_hash = st.session_state.pending_audio_hash
    st.session_state.pending_audio_bytes = None
    st.session_state.pending_audio_hash = None
    st.rerun()
# Audio Recorder Widget
st.write("\n")
st.write("### 1. Record Audio (You can record multiple parts)")

# Give the widget a dynamic key so we can force it to reset
new_audio = st.audio_input(
    "Dictate your notes here:",
    key=f"audio_input_{st.session_state.audio_key}",
)
# If new audio is recorded, stage it for user confirmation.
if new_audio is not None:
    recorded_bytes = new_audio.getvalue()
    if not recorded_bytes:
        st.warning("Recording received 0 bytes. Please try again (network/browser may have interrupted the upload).")
    else:
        recorded_hash = hashlib.sha256(recorded_bytes).hexdigest()
        if recorded_hash != st.session_state.last_recorded_hash and recorded_hash != st.session_state.pending_audio_hash:
            if recording_mode == "Quick":
                st.session_state.audio_chunks.append(recorded_bytes)
                st.session_state.last_recorded_hash = recorded_hash
            else:
                st.session_state.pending_audio_bytes = recorded_bytes
                st.session_state.pending_audio_hash = recorded_hash
if recording_mode == "Regular" and st.session_state.pending_audio_bytes:
    size_mb = len(st.session_state.pending_audio_bytes) / (1024 * 1024)
    st.info(
        f"Latest clip received: {size_mb:.2f} MB. Click **Add clip** to append it to your dictation. "
        "If you are not happy with it, **record again**—that replaces this clip until you add it."
    )
    if st.button("Add clip", type="primary", use_container_width=True):
        st.session_state.audio_chunks.append(st.session_state.pending_audio_bytes)
        st.session_state.last_recorded_hash = st.session_state.pending_audio_hash
        st.session_state.pending_audio_bytes = None
        st.session_state.pending_audio_hash = None
        st.rerun()
# Display how many clips have been recorded
if st.session_state.audio_chunks:
    st.success(f"🎙️ {len(st.session_state.audio_chunks)} audio segment(s) recorded.")
    col_proc, col_clear = st.columns(2)
    with col_proc:
        process_clicked = st.button("Process Full Dictation", type="primary", use_container_width=True)
    with col_clear:
        if st.button("Clear Recordings & Start Over", use_container_width=True):
            st.session_state.audio_chunks = []
            st.session_state.last_recorded_hash = None
            st.session_state.pending_audio_bytes = None
            st.session_state.pending_audio_hash = None
            st.session_state.audio_key += 1
            st.session_state.last_audio = None
            st.session_state.transcription = ""
            st.session_state.pro_version = ""
            st.session_state.report_version = ""
            st.rerun()
    if process_clicked:
        if not API_KEY or "sk-sk" in API_KEY:
            st.warning("⚠️ The provided API key is invalid or incomplete.")
        else:
            with st.spinner(f"Combining audio natively, transcribing with {selected_model}, and processing notes..."):
                try:
                    final_audio_bytes = stitch_audio_chunks(st.session_state.audio_chunks)
                    transcription, pro_version, report_version = process_audio(
                        API_KEY,
                        final_audio_bytes,
                        selected_model,
                        report_type,
                    )
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
    save_choice = st.radio(
        "Which version would you like to save to your history?",
        ("Professional Clinical Version", "Radiology Report Version"),
        horizontal=True,
    )
    if st.button("Save Selected Version"):
        text_to_save = (
            st.session_state.pro_version
            if save_choice == "Professional Clinical Version"
            else st.session_state.report_version
        )
        st.session_state.history.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %I:%M %p"),
                "original": st.session_state.transcription,
                "choice": save_choice,
                "saved_text": text_to_save,
            }
        )
        st.session_state._show_save_toast = True
        st.rerun()
