from pytube import YouTube
import streamlit as st

# Title of the app
st.title("_____________________")

# Text input for YouTube URL
youtube_url = st.text_input("Enter YouTube Video URL:")

# Check if a URL has been provided
if youtube_url:
    yt = YouTube(youtube_url)
    st.write(f"Video Title: {video_title}")
