#!/usr/bin/env python3
"""Test current YouTube token capabilities"""

import os
import json
import urllib.request
import urllib.parse
from datetime import datetime

YOUTUBE_TOKEN_FILE = "/data/workspace/youtube_tokens.json"

# Load .env
with open('/data/workspace/.env') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, _, v = line.partition('=')
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")

def get_valid_access_token():
    with open(YOUTUBE_TOKEN_FILE) as f:
        tokens = json.load(f)
    
    expires_at = tokens.get('expires_at', 0)
    
    if datetime.now().timestamp() < expires_at - 300:
        print("✓ Token masih valid (belum expired)")
        return tokens['access_token']
    
    print("⟳ Refreshing token...")
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': tokens['refresh_token'],
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    
    req = urllib.request.Request(
        'https://oauth2.googleapis.com/token',
        data=urllib.parse.urlencode(data).encode(),
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    
    with urllib.request.urlopen(req) as response:
        new_tokens = json.loads(response.read().decode())
    
    tokens['access_token'] = new_tokens['access_token']
    tokens['expires_at'] = datetime.now().timestamp() + new_tokens.get('expires_in', 3600)
    
    with open(YOUTUBE_TOKEN_FILE, 'w') as f:
        json.dump(tokens, f, indent=2)
    
    print("✓ Token berhasil di-refresh")
    return tokens['access_token']

def call_youtube_api(access_token, endpoint, params=None):
    """Helper to call YouTube API"""
    base_url = "https://www.googleapis.com/youtube/v3"
    url = f"{base_url}/{endpoint}"
    
    if params:
        url += "?" + urllib.parse.urlencode(params)
    
    req = urllib.request.Request(
        url,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode()), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}: {e.read().decode()}"

# === TEST ===
print("=" * 50)
print("TEST YOUTUBE TOKEN CAPABILITIES")
print("=" * 50)

access_token = get_valid_access_token()
print()

# Test 1: channels.list (mine=true) - basic read
print("[1] Test channels.list (mine=true)...")
result, error = call_youtube_api(access_token, "channels", {
    "part": "snippet,statistics",
    "mine": "true"
})
if result:
    channel = result['items'][0]
    print(f"   ✓ Berhasil. Channel: {channel['snippet']['title']}")
    print(f"   Subscribers: {channel['statistics'].get('subscriberCount', 'N/A')}")
else:
    print(f"   ✗ Gagal: {error}")

print()

# Test 2: Search my videos (read)
print("[2] Test search (my recent videos)...")
result, error = call_youtube_api(access_token, "search", {
    "part": "snippet",
    "forMine": "true",
    "maxResults": "3",
    "order": "date",
    "type": "video"
})
if result:
    print(f"   ✓ Berhasil. Ditemukan {len(result.get('items', []))} video")
else:
    print(f"   ✗ Gagal: {error}")

print()

# Test 3: Playlist access (membutuhkan scope lebih tinggi)
print("[3] Test playlist access (mine=true)...")
result, error = call_youtube_api(access_token, "playlists", {
    "part": "snippet",
    "mine": "true",
    "maxResults": "3"
})
if result:
    print(f"   \u2713 Berhasil. Ditemukan {len(result.get('items', []))} playlist")
else:
    print(f"   \u2717 Gagal: {error}")

print()
print("=" * 50)
print("Test selesai.")
print("=" * 50)