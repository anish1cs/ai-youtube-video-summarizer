import streamlit as st
import pyperclip

from src.transcript_extractor import extract_video_id, fetch_transcript, transcript_to_text
from src.summarizer import summarize_text
from src.keyword_extractor import extract_keywords
from src.utils import save_history

st.set_page_config(page_title="YouTube Video Summarizer", layout="centered")
st.title("🎬 AI-Powered YouTube Video Summarizer")

# Input section
video_url = st.text_input("Enter a YouTube video URL")
summary_length = st.slider("Choose summary length (approx. words)", 60, 300, 150, step=10)

if st.button("Summarize Video"):
    video_id = extract_video_id(video_url)
    if not video_id:
        st.error("Invalid YouTube URL.")
    else:
        with st.spinner("Extracting transcript..."):
            transcript = fetch_transcript(video_id)
        if not transcript:
            st.error("Transcript could not be fetched. Video may not have subtitles.")
        else:
            text = transcript_to_text(transcript)
            if not text.strip():
                st.error("Transcript is empty.")
            else:
                with st.spinner("Summarizing..."):
                    summary = summarize_text(text, length=summary_length)
                st.subheader("Summary")
                st.text_area("Summary Text", value=summary, height=200, key="summary_box")
                if st.button("Copy to Clipboard"):
                    pyperclip.copy(summary)
                    st.success("Copied to clipboard!")
                keywords = extract_keywords(summary)
                st.subheader("Key Topics")
                st.write(", ".join(keywords))
                save_history(video_url, summary, keywords)
