from pytube import YouTube
import streamlit as st
from langcodes import Language

# Get a list of all language codes
def get_all_languages():
    languages = {}
    for lang in Language.list():
        languages[lang.language] = lang.language
    return languages

# Streamlit app
def main():
    
    # Title of the app
    st.title("_____________________")

    # Text input for YouTube URL
    youtube_url = st.text_input("Enter YouTube Video URL:")

    # Create toggle list for languages
    selected_languages = []
    for language_name, language_code in languages.items():
        if st.checkbox(f'Select {language_name}', value=False):
            selected_languages.append(language_code)

    # Check if a URL has been provided
    if youtube_url:
        yt = YouTube(youtube_url)
        st.subheader(yt.title)
    
if __name__ == "__main__":
    main()
