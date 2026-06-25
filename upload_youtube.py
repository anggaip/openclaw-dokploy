#!/usr/bin/env python3
"""YouTube video upload script with robust token handling + proper upload scope."""

import json
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request


def load_and_normalize_credentials():
    """Load token and normalize format + refresh if needed."""
    tokens_path = "/data/workspace/youtube_tokens.json"
    
    if not os.path.exists(tokens_path):
        print("ERROR: youtube_tokens.json not found")
        print("   Run: python3 /data/workspace/youtube_oauth_setup.py")
        return None
    
    with open(tokens_path) as f:
        token_data = json.load(f)
    
    # Normalize old format ("token" -> "access_token")
    if "token" in token_data and "access_token" not in token_data:
        token_data["access_token"] = token_data.pop("token")
    
    # Ensure client credentials are present
    if "client_id" not in token_data or not token_data.get("client_id"):
        with open(".env") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    if k.strip() == "YOUTUBE_CLIENT_ID":
                        token_data["client_id"] = v.strip().strip('"').strip("'")
                    if k.strip() == "YOUTUBE_CLIENT_SECRET":
                        token_data["client_secret"] = v.strip().strip('"').strip("'")
    
    if "token_uri" not in token_data:
        token_data["token_uri"] = "https://oauth2.googleapis.com/token"
    
    creds = Credentials.from_authorized_user_info(token_data)
    
    # Refresh if expired
    if creds.expired and creds.refresh_token:
        print("Token expired, refreshing...")
        try:
            creds.refresh(Request())
            refreshed = json.loads(creds.to_json())
            refreshed["client_id"] = token_data.get("client_id")
            refreshed["client_secret"] = token_data.get("client_secret")
            refreshed["token_uri"] = "https://oauth2.googleapis.com/token"
            with open(tokens_path, "w") as f:
                json.dump(refreshed, f, indent=2)
            print("Token refreshed")
        except Exception as e:
            print(f"Failed to refresh: {e}")
            return None
    
    return creds


def upload_video(video_path, title, description="", tags=None, category_id="27", privacy_status="private"):
    creds = load_and_normalize_credentials()
    if not creds:
        return False
    
    youtube = build("youtube", "v3", credentials=creds)
    
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or [],
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status,
            "selfDeclaredMadeForKids": False
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    
    print(f"Uploading {video_path} ...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"   Progress: {int(status.progress() * 100)}%")
    
    video_id = response["id"]
    print("")
    print("Upload successful!")
    print(f"   Video ID: {video_id}")
    print(f"   URL: https://youtu.be/{video_id}")
    print(f"   Privacy: {privacy_status}")
    return video_id


if __name__ == "__main__":
    # Test upload
    upload_video(
        video_path="/data/workspace/night_city_preview.webm",
        title="Test Upload via MISO Agent - Short Video",
        description="""Testing YouTube Shorts upload from AI agent.

#Shorts #Test""",
        tags=["test", "shorts", "ai", "agent"],
        category_id="27",
        privacy_status="private"
    )
