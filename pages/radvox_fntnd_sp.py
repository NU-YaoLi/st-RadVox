import streamlit as st

st.set_page_config(page_title="Surprise", layout="centered")

if st.button("Back", use_container_width=True):
    try:
        st.switch_page("radvox_fntnd.py")
    except Exception:
        st.error("Couldn't navigate back. Try using the sidebar page selector.")

st.title("Surprise")
st.video("media/J&J.mp4")

