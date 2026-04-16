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

        [data-testid="stMainBlockContainer"] {{
            max-width: 1200px !important;
            padding-top: 2rem;
        }}
        {extra}
        </style>
        """,
        unsafe_allow_html=True,
    )
