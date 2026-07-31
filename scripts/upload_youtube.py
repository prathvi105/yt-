"""
Step 5: Upload final_video.mp4 to YouTube as a Short.
Needs YT_CLIENT_SECRET + YT_REFRESH_TOKEN env vars (OAuth, generated once locally).
"""
import os, json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload():
    with open("assets/content.json", encoding="utf-8") as f:
        content = json.load(f)

    creds = Credentials(
        token=None,
        refresh_token=os.environ["YT_REFRESH_TOKEN"],
        client_id=os.environ["YT_CLIENT_ID"],
        client_secret=os.environ["YT_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
    )

    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": content["caption"].split("#")[0].strip()[:95] + " #Shorts",
            "description": content["caption"],
            "tags": ["shorts", "cute", "viral", "kuchupuchu"],
            "categoryId": "24",
        },
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
    }

    media = MediaFileUpload("assets/final_video.mp4", mimetype="video/mp4", resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = request.execute()
    print("Uploaded:", response.get("id"))

if __name__ == "__main__":
    upload()
