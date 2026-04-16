import streamlit as st

st.set_page_config(page_title="Surprise", layout="centered")

top_left, _ = st.columns([1, 6])
with top_left:
    if st.button("Back", use_container_width=True):
        st.switch_page("radvox_fntnd.py")

st.title("Surprise")
st.video("media/J&J.mp4")

