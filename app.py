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
        # Check if a URL has been provided
    if youtube_url:
        try:
            yt = YouTube(youtube_url)
            st.subheader(yt.title)
        except Exception as e:
            st.warning(f"Failed to fetch video details: {e}")
            return

        if language_code:
            try:
                caption = yt.captions.get_by_language_code(language_code)
                subtitles = caption.generate_srt_captions()
                st.text_area("Subtitles", subtitles)
            except Exception as e1:
                    try:
                        caption = yt.captions.get_by_language_code(fallback_language_code)
                        subtitles = caption.generate_srt_captions()
                        st.text_area("Subtitles", subtitles)
                    except Exception as e2:
                        st.warning(f"Failed to retrieve captions: {e2}")
        else:
            st.warning("Please enter a language code.")
    
if __name__ == "__main__":
    main()
