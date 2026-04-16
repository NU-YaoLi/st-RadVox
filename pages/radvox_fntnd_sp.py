import streamlit as st

st.set_page_config(page_title="Surprise", layout="centered")

st.markdown(
    """
    <style>
    /* Hide multipage navigation (left menu) */
    [data-testid="stSidebarNav"] { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

if st.button("Back", use_container_width=True):
    try:
        st.switch_page("radvox_fntnd.py")
    except Exception:
        st.error("Couldn't navigate back. Try using the sidebar page selector.")

st.title("Surprise")
_, center_col, _ = st.columns([1, 3, 1])
with center_col:
    st.video("media/J&J.mp4")

