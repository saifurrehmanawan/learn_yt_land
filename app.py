from pytube import YouTube
import streamlit as st
from langcodes import Language

# Streamlit app
def main():
    
    # Title of the app
    st.title("_____________________")

    # Text input for YouTube URL
    youtube_url = st.text_input("Enter YouTube Video URL:")
    language_code = st.text_input("Enter the language code (e.g., 'en' for English, 'es' for Spanish):")

    # Check if a URL has been provided
    if youtube_url and language_code:
        yt = YouTube(youtube_url)
        st.subheader(yt.title)
    
if __name__ == "__main__":
    main()
