from pytubefix import YouTube
import streamlit as st

# Streamlit app
def main():
    
    # Title of the app
    st.title("YouTube Video Subtitle Navigator")

    # Text input for YouTube URL
    youtube_url = st.text_input("Enter YouTube Video URL:")
    language_code = st.text_input("Enter the language code (e.g., 'en' for English, 'es' for Spanish):")

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
            except Exception as e1:
                try:
                    caption = yt.captions.get_by_language_code(f"a.{language_code}")
                    subtitles = caption.generate_srt_captions()
                except Exception as e2:
                    st.warning(f"Failed to retrieve captions: {e2}")
                    return
            
            # Split subtitles into individual segments
            subtitle_segments = subtitles.split('\n\n')
            total_segments = len(subtitle_segments)
            if 'current_segment' not in st.session_state:
                st.session_state.current_segment = 0

            # Display current subtitle segment
            current_segment = subtitle_segments[st.session_state.current_segment]
            st.write(current_segment)
            
            # Extract start and end times for the current subtitle
            try:
                start_time, end_time = current_segment.split('\n')[1].split(' --> ')
                start_time_seconds = sum(float(x) * 60 ** i for i, x in enumerate(reversed(start_time.replace(',', '.').split(':'))))
                end_time_seconds = sum(float(x) * 60 ** i for i, x in enumerate(reversed(end_time.replace(',', '.').split(':'))))
            except IndexError:
                st.warning("Failed to parse subtitle timings.")
                return

            # Display video frame with st.video
            # HTML code to embed the video with JavaScript for looping playback
            video_html = f"""
<div>
  <iframe id="video" width="560" height="315" src="{video_url}?start={start_time_seconds}&autoplay=1&mute=1" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
</div>
<script>
  const video = document.getElementById('video');
  video.addEventListener('load', function() {{
    video.contentWindow.postMessage('{"event":"command","func":"seekTo","args":[{start_time_seconds}, true]}', '*');
  }});

  video.addEventListener('timeupdate', function() {{
    const currentTime = video.contentWindow.postMessage('{"event":"command","func":"getCurrentTime","args":""}', '*');
    if (currentTime >= {end_time_seconds}) {{
      video.contentWindow.postMessage('{"event":"command","func":"seekTo","args":[{start_time_seconds}, true]}', '*');
    }}
  }});
</script>
"""

        # Display the video in Streamlit
        st.markdown(video_html, unsafe_allow_html=True)

            # Navigation buttons
            col1, col2 = st.columns([1, 1])
            if col1.button("Previous"):
                if st.session_state.current_segment > 0:
                    st.session_state.current_segment -= 1
                    st.experimental_rerun()

            if col2.button("Next"):
                if st.session_state.current_segment < total_segments - 1:
                    st.session_state.current_segment += 1
                    st.experimental_rerun()

        else:
            st.warning("Please enter a language code.")
    
if __name__ == "__main__":
    main()
