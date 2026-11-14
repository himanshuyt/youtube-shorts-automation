import os
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
IST = ZoneInfo("Asia/Kolkata")

def youtube_client():
    required = ["YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"]
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        raise RuntimeError("Missing GitHub Secrets: " + ", ".join(missing))
    credentials = Credentials(
        token=None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
        scopes=SCOPES
    )
    return build("youtube", "v3", credentials=credentials, cache_discovery=False)

def next_publish_time_ist():
    now = datetime.now(IST)
    publish_at = now.replace(hour=19, minute=0, second=0, microsecond=0)
    if publish_at <= now:
        publish_at += timedelta(days=1)
    return publish_at.isoformat()

def upload_video(video_path, metadata, schedule_public=False):
    youtube = youtube_client()
    # Scheduled videos must be uploaded as private with a future publishAt timestamp.
    status = {"privacyStatus": "private", "selfDeclaredMadeForKids": False}
    if schedule_public:
        status["publishAt"] = next_publish_time_ist()
    body = {
        "snippet": {
            "title": metadata["title"],
            "description": metadata["description"] + "\n\n#Shorts",
            "tags": metadata["tags"] + ["Shorts"],
            "categoryId": "20"
        },
        "status": status
    }
    media = MediaFileUpload(str(video_path), mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        _, response = request.next_chunk()
    return {"video_id": response["id"], "publish_at": status.get("publishAt")}
