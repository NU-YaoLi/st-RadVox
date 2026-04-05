# Open Terminal: Press Command + Space, type Terminal, and hit Enter.
# Check for Homebrew: Type brew -v and hit Enter.
# If it shows a version number, skip to Step 3.
# If it says "command not found," paste this and hit Enter:
# /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
# brew install ffmpeg
# pip3 install streamlit openai pydub

# Verify: Once finished, type ffmpeg -version. If you see FFmpeg version 8.1 "Hoare" (the March 2026 release) or similar, you are good to go!

# pkill -f streamlit
# python3 -m streamlit run /Applications/myDic.py &>/dev/null & disown
# streamlit run myDic.py
# Note: Since this uses browser-based recording, you do not need to install OS-level audio dependencies.

import streamlit as st
from datetime import datetime
from pydub import AudioSegment
import io
from voxrad_bknd import process_audio  # Importing the backend function

# MacOS ffmpeg setup
# AudioSegment.converter = "/opt/homebrew/bin/ffmpeg"

# --- Configuration & Setup ---
st.set_page_config(page_title="Vet Radiology Voice Assistant", layout="centered")

st.markdown(
    """
    <style>
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
# If not found, it returns an empty string to gracefully trigger the warning below
API_KEY = st.secrets.get("OPENAI_API_KEY", "") 

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
if "grammar_version" not in st.session_state:
    st.session_state.grammar_version = ""
if "pro_version" not in st.session_state:
    st.session_state.pro_version = ""
if "history" not in st.session_state:
    st.session_state.history = []

# --- Sidebar: History ---
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
# Top Section layout with Title on left and Model Selector on right
title_col, toggle_col = st.columns([3, 1])

with title_col:
    st.title("🎙️ Vet Radiology Voice Assistant")
    st.write("Record your radiology notes below to generate transcribed, grammar-corrected, and professional clinical versions.")

with toggle_col:
    # Add some padding to push it down slightly so it aligns nicely with the title
    st.write("\n") 
    st.write("\n")
    st.write("\n") 
    selected_model = st.radio(
        "Transcription Model:",
        ("gpt-4o-transcribe", "whisper-1"),
        index=0
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
            st.session_state.grammar_version = ""
            st.session_state.pro_version = ""
            
            st.rerun()

    if process_clicked:
        if API_KEY.startswith("sk-sk") or API_KEY == "" or API_KEY == "YOUR_REAL_API_KEY_HERE":
            st.warning("⚠️ You are currently using the dummy API key or no key was found in secrets. The app will fail to transcribe.")
            
        with st.spinner(f"Combining audio, transcribing with {selected_model}, and processing notes..."):
            try:
                # Stitch the audio chunks together using pydub
                combined_audio = AudioSegment.empty()
                for chunk in st.session_state.audio_chunks:
                    segment = AudioSegment.from_file(io.BytesIO(chunk), format="wav")
                    combined_audio += segment
                
                # Export the combined audio back to bytes so process_audio can use it
                combined_io = io.BytesIO()
                combined_audio.export(combined_io, format="wav")
                final_audio_bytes = combined_io.getvalue()

                # Pass the combined audio to the backend function
                transcription, grammar_version, pro_version = process_audio(API_KEY, final_audio_bytes, selected_model)
                
                # Save all results to session state
                st.session_state.last_audio = final_audio_bytes
                st.session_state.transcription = transcription
                st.session_state.grammar_version = grammar_version
                st.session_state.pro_version = pro_version
                
            except Exception as e:
                st.error(f"An API error occurred.\n\nError details: {e}")

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
        st.subheader("Grammar Corrected Version")
        st.text(st.session_state.grammar_version)
        
    with col2:
        st.subheader("Professional Clinical Version")
        st.text(st.session_state.pro_version) 

    st.write("\n")
    st.write("---")
    st.write("### 4. Save to History")
    
    # Selection mechanism for saving
    save_choice = st.radio(
        "Which version would you like to save to your history?",
        ("Grammar Corrected Version", "Professional Version"),
        horizontal=True
    )
    
    if st.button("Save Selected Version"):
        # Determine which text to save based on the radio button choice
        text_to_save = st.session_state.grammar_version if save_choice == "Grammar Corrected Version" else st.session_state.pro_version
        
        # Append to the history list
        st.session_state.history.append({
            "timestamp": datetime.now().strftime("%I:%M %p"),
            "original": st.session_state.transcription,
            "choice": save_choice,
            "saved_text": text_to_save
        })
        
        st.toast("Saved successfully! Check the sidebar.")
        st.rerun()