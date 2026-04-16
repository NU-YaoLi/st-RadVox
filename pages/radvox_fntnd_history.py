import streamlit as st

from radvox_sidebar import go_to_main_page, render_sidebar_nav_and_settings

st.set_page_config(page_title="RadVox: Conversion History", layout="centered")

st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] { display: none; }

    [data-testid="stMainBlockContainer"] {
        max-width: 1200px !important;
        padding-top: 2rem;
    }

    .stText {
        white-space: pre-wrap !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "history" not in st.session_state:
    st.session_state.history = []

render_sidebar_nav_and_settings()

if st.button("← Back to voice assistant", use_container_width=True):
    go_to_main_page()

st.title("📚 Conversion History")

if not st.session_state.history:
    st.info("No saved records yet. Transcribe and save audio on the main page to see history here.")
else:
    for record in reversed(st.session_state.history):
        with st.expander(f"Record: {record['timestamp']}"):
            st.write("**Original Transcript:**")
            st.text(record["original"])
            st.write(f"**Saved Version ({record['choice']}):**")
            st.text(record["saved_text"])
