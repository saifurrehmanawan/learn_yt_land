from pytubefix import YouTube
import streamlit as st
import streamlit.components.v1 as components

# Streamlit app
def main():
    st.title("YouTube Video Subtitle Navigator")

    # Text input for YouTube URL
    youtube_url = st.text_input("Enter YouTube Video URL:")
    language_code = st.text_input("Enter the language code (e.g., 'en' for English, 'es' for Spanish):")

    # Check if a URL has been provided
    if youtube_url and language_code:
        try:
            yt = YouTube(youtube_url)
            st.subheader(yt.title)
            
            caption = yt.captions.get_by_language_code(language_code) or yt.captions.get_by_language_code(f"a.{language_code}")
            subtitles = caption.generate_srt_captions()

            # Split subtitles into individual segments
            subtitle_segments = subtitles.split('\n\n')
            total_segments = len(subtitle_segments)

            if 'current_segment' not in st.session_state:
                st.session_state.current_segment = 0

            # Display current subtitle segment
            current_segment = subtitle_segments[st.session_state.current_segment]
            st.write(current_segment)
            
            # Extract start and end times for the current subtitle
            start_time, end_time = current_segment.split('\n')[1].split(' --> ')
            start_time_seconds = sum(float(x) * 60 ** i for i, x in enumerate(reversed(start_time.replace(',', '.').split(':'))))
            end_time_seconds = sum(float(x) * 60 ** i for i, x in enumerate(reversed(end_time.replace(',', '.').split(':'))))
            
            # Display video frame and playback controls
            video_url = yt.watch_url
            components.html(f"""
                <video id="video" width="640" height="360" controls>
                    <source src="{video_url}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
                <script>
                    var video = document.getElementById('video');
                    video.currentTime = {start_time_seconds};
                    video.ontimeupdate = function() {{
                        if (video.currentTime >= {end_time_seconds}) {{
                            video.pause();
                        }}
                    }};
                </script>
            """, height=400)

            # Navigation buttons
            col1, col2 = st.columns([1, 1])
            if col1.button("Previous") and st.session_state.current_segment > 0:
                st.session_state.current_segment -= 1
                st.experimental_rerun()

            if col2.button("Next") and st.session_state.current_segment < total_segments - 1:
                st.session_state.current_segment += 1
                st.experimental_rerun()

        except Exception as e:
            st.warning(f"Failed to retrieve captions or video details: {e}")

if __name__ == "__main__":
    main()
