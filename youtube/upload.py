import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

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

def upload_video(video_path, metadata, publish_public=False):
    youtube = youtube_client()
    status = {"privacyStatus": "public" if publish_public else "private", "selfDeclaredMadeForKids": False}
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
    return response["id"]
