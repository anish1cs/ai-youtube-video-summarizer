import re
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound
)

def extract_video_id(url: str) -> str:
    """
    Extract the YouTube video ID from various URL formats.
    """
    patterns = [
        r'(?:https?://)?(?:www\.)?youtu\.be/([^?&]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([^?&]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([^?&]+)',
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([^?&]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_transcript(video_id: str, language: str = 'en'):
    """
    Fetch transcript from YouTube for videos that already have subtitles.
    Tries human first, then auto-generated, otherwise returns None.
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        # Print available transcript languages
        print("\nAvailable transcripts:")
        for t in transcript_list:
            t_type = "Auto-generated" if t.is_generated else "Human"
            print(f"- {t.language_code} ({t.language}) [{t_type}]")

        # Try human transcript first
        try:
            transcript = transcript_list.find_transcript([language])
            print(f"\nUsing human transcript in '{language}'")
            return transcript.fetch()
        except NoTranscriptFound:
            pass

        # Try auto-generated transcript
        try:
            transcript = transcript_list.find_generated_transcript([language])
            print(f"\nUsing auto-generated transcript in '{language}'")
            return transcript.fetch()
        except NoTranscriptFound:
            pass

        return None
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
    except Exception as e:
        print(f"[ERROR] Transcript extraction failed: {e}")
        return None


def transcript_to_text(transcript) -> str:
    """
    Convert transcript list into a single string.
    """
    if not transcript:
        return ""
    return " ".join(entry['text'] for entry in transcript)


if __name__ == "__main__":
    url = input("Enter YouTube URL: ").strip()
    vid = extract_video_id(url)

    if not vid:
        print("Invalid YouTube URL format.")
    else:
        transcript = fetch_transcript(vid)
        if transcript:
            print("\nTranscript sample:", transcript[:3])  # First 3 entries
            print("\nFull text preview:\n", transcript_to_text(transcript)[:500], "...")
        else:
            print("Transcript could not be fetched. Video may not have subtitles.")
