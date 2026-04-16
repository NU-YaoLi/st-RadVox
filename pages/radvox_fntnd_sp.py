import streamlit as st

from radvox_sidebar import go_to_main_page
from radvox_ui import inject_base_css

st.set_page_config(page_title="Surprise", layout="centered")

inject_base_css(include_st_text_pre_wrap=False)

back_col, _ = st.columns([2, 8])
with back_col:
    if st.button("← Back to Voice Assistant", use_container_width=True):
        go_to_main_page()

st.title("Surprise")
_, center_col, _ = st.columns([1, 3, 1])
with center_col:
    st.video("media/J&J.mp4")
