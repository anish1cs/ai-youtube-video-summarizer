import os
import json

def save_history(video_url, summary, keywords):
    history_file = "history.json"
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = []
    data.append({
        "video_url": video_url,
        "summary": summary,
        "keywords": keywords
    })
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
