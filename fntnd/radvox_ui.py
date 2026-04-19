"""Shared Streamlit UI helpers (CSS injection)."""

from __future__ import annotations

import streamlit as st


def inject_base_css(*, include_st_text_pre_wrap: bool = False) -> None:
    """Hide default multipage nav, widen main block; optionally preserve newlines in st.text."""
    extra = """
    .stText {
        white-space: pre-wrap !important;
    }
    """ if include_st_text_pre_wrap else ""

    st.markdown(
        f"""
        <style>
        [data-testid="stSidebarNav"] {{ display: none; }}

        /* Extra top padding clears Streamlit’s app header / toolbar so the first
           row (e.g. Back) is not clipped under fixed chrome. */
        [data-testid="stMainBlockContainer"] {{
            max-width: 1200px !important;
            padding-top: clamp(3.5rem, 10vh, 6rem) !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}

        /* Column wrappers sometimes clip children at the top edge. */
        [data-testid="stMainBlockContainer"] [data-testid="column"] {{
            overflow: visible !important;
        }}
        {extra}
        </style>
        """,
        unsafe_allow_html=True,
    )
