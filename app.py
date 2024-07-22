from pytubefix import YouTube
import streamlit as st

# Streamlit app
def main():
    
    # Title of the app
    st.title("_____________________")

    # Text input for YouTube URL
    youtube_url = st.text_input("Enter YouTube Video URL:")
    language_code = st.text_input("Enter the language code (e.g., 'en' for English, 'es' for Spanish):")

    # Check if a URL has been provided
    if youtube_url and language_code:
        try:
            yt = YouTube(youtube_url)
            st.subheader(yt.title)
        except Exception as e:
            st.warning("Please enter a valid YouTube link.")

        try:
            caption = yt.captions.get_by_language_code(language_code)
            subtitles = caption.generate_srt_captions()
        except Exception as e1:  # Replace with the specific error you're expecting
            try:
                caption = yt.captions.get_by_language_code(a.language_code)
                subtitles = caption.generate_srt_captions()
            except Exception as e2:  # Replace with another specific error you're expecting
                st.warning("Failed to retrieve caption.")
    
if __name__ == "__main__":
    main()
