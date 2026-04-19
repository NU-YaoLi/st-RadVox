import sys
from pathlib import Path

# pages/ is under fntnd/; repo root is two levels up (where media/ lives).
_REPO_ROOT = Path(__file__).resolve().parents[2]
_rs = str(_REPO_ROOT)
if _rs not in sys.path:
    sys.path.insert(0, _rs)

import streamlit as st

from fntnd.radvox_sidebar import go_to_main_page
from fntnd.radvox_ui import inject_base_css

st.set_page_config(page_title="Surprise", layout="centered")

inject_base_css(include_st_text_pre_wrap=False)

back_col, _ = st.columns([2, 8])
with back_col:
    if st.button("← Back to Voice Assistant", use_container_width=True):
        go_to_main_page()

st.title("Surprise")
_, center_col, _ = st.columns([1, 3, 1])
_video = _REPO_ROOT / "media" / "J&J.mp4"
with center_col:
    if _video.is_file():
        st.video(str(_video))
    else:
        st.error(
            f"Video not found at `{_video}`. Ensure `media/J&J.mp4` is committed in the repo root (not under fntnd/)."
        )
