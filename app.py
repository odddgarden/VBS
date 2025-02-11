import streamlit as st

# Set page configuration
st.set_page_config(page_title="PRINCESS MOVIE WORLD", layout="centered")

# Page title
st.markdown("""
    <h1 style='text-align: center;'>NOW SHOWING GUSTO MANOOD NI PRINCESS KARYONSI NG ANORA</h1>
""", unsafe_allow_html=True)

# Embed the movie iframe
tt_id = "tt28607951"  # IMDb ID of the movie
embed_url = f"https://vidsrc.xyz/embed/movie?imdb={tt_id}"

st.markdown(
    f'<iframe src="{embed_url}" width="80%" height="500px" style="border:none;"></iframe>',
    unsafe_allow_html=True
)
