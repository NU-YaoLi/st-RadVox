import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_rs = str(_REPO_ROOT)
if _rs not in sys.path:
    sys.path.insert(0, _rs)

import streamlit as st

from fntnd.radvox_sidebar import go_to_main_page
from fntnd.radvox_ui import inject_base_css

st.set_page_config(page_title="RadVox: Transcription History", layout="centered")

inject_base_css(include_st_text_pre_wrap=True)

if "history" not in st.session_state:
    st.session_state.history = []

back_col, _ = st.columns([2, 8])
with back_col:
    if st.button("← Back to Voice Assistant", use_container_width=True):
        go_to_main_page()

st.title("Transcription History")

if not st.session_state.history:
    st.info("No saved records yet. Transcribe and save audio on the main page to see history here.")
else:
    for record in reversed(st.session_state.history):
        with st.expander(f"Record: {record['timestamp']}"):
            st.write("**Original Transcript:**")
            st.text(record["original"])
            st.write(f"**Saved Version ({record['choice']}):**")
            st.text(record["saved_text"])
