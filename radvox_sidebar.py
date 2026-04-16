"""Shared sidebar: navigation + application settings (persists across multipage sessions)."""

from __future__ import annotations

import streamlit as st


def go_to_surprise_page() -> None:
    for target in ("pages/radvox_fntnd_sp.py", "radvox_fntnd_sp.py"):
        try:
            st.switch_page(target)
            return
        except Exception:
            continue
    st.error("Couldn't navigate to the Surprise page. Make sure `pages/radvox_fntnd_sp.py` exists.")


def go_to_history_page() -> None:
    for target in ("pages/radvox_fntnd_history.py", "radvox_fntnd_history.py"):
        try:
            st.switch_page(target)
            return
        except Exception:
            continue
    st.error("Couldn't navigate to History. Make sure `pages/radvox_fntnd_history.py` exists.")


def go_to_main_page() -> None:
    try:
        st.switch_page("radvox_fntnd.py")
    except Exception:
        st.error("Couldn't navigate to the main app. Run Streamlit from the project root.")


def render_sidebar_nav_and_settings() -> tuple[str, str, str]:
    """Surprise + History buttons, then settings radios. Returns (model, report_type, recording_mode)."""
    if st.sidebar.button("surprise", use_container_width=True):
        go_to_surprise_page()
    if st.sidebar.button("History", use_container_width=True):
        go_to_history_page()

    st.sidebar.divider()
    st.sidebar.markdown("**Application settings**")
    selected_model = st.sidebar.radio(
        "Transcription Model:",
        ("gpt-4o-transcribe", "whisper-1"),
        key="radvox_setting_model",
    )
    report_type = st.sidebar.radio(
        "Report Type:",
        ("CT", "US"),
        key="radvox_setting_report",
    )
    recording_mode = st.sidebar.radio(
        "Recording Mode:",
        ("Quick", "Regular"),
        key="radvox_setting_recording",
        help="Quick: each new recording is added automatically. Regular: confirm each clip with Add clip (re-record replaces the clip you have not added yet).",
    )
    return selected_model, report_type, recording_mode
