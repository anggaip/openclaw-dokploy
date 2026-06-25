#!/usr/bin/env python3
"""
YouTube OAuth Setup Script
Creates fresh OAuth tokens for YouTube (with upload support)
"""

import os
import json
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from datetime import datetime

# Load .env file manually
def load_env(path):
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")

load_env('/data/workspace/.env')

YOUTUBE_TOKEN_FILE = "/data/workspace/youtube_tokens.json"
REDIRECT_URI = "http://localhost:8888"

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/yt-analytics-monetary.readonly",
]

CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    print("❌ ERROR: YOUTUBE_CLIENT_ID or YOUTUBE_CLIENT_SECRET not set in .env")
    exit(1)

print(f"✅ Client ID: {CLIENT_ID[:25]}...")

class OAuthHandler(BaseHTTPRequestHandler):
    code = None
    
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        
        if 'code' in query:
            OAuthHandler.code = query['code'][0]
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.end_headers()
            self.wfile.write(b"<h1>Authorization Successful! You can close this tab.</h1>")
        else:
            self.send_response(400)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass

def get_auth_url():
    params = {
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'response_type': 'code',
        'scope': ' '.join(SCOPES),
        'access_type': 'offline',
        'prompt': 'consent',
    }
    return "https://accounts.google.com/o/oauth2/auth?" + urllib.parse.urlencode(params)

def exchange_code_for_tokens(code):
    data = {
        'code': code,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    
    req = urllib.request.Request(
        'https://oauth2.googleapis.com/token',
        data=urllib.parse.urlencode(data).encode(),
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )
    
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode())

def main():
    print("=" * 70)
    print("YouTube OAuth Setup (Upload Enabled)")
    print("=" * 70)
    
    # Backup old token
    if os.path.exists(YOUTUBE_TOKEN_FILE):
        backup = f"{YOUTUBE_TOKEN_FILE}.backup.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        print(f"📦 Backing up old token to: {backup}")
        os.rename(YOUTUBE_TOKEN_FILE, backup)
    
    # Start server
    server = HTTPServer(('localhost', 8888), OAuthHandler)
    Thread(target=server.serve_forever, daemon=True).start()
    print("🔌 Callback server started")
    
    auth_url = get_auth_url()
    print("\n" + "=" * 70)
    print("🔗 COPY THIS AUTHORIZATION URL:")
    print("=" * 70)
    print(auth_url)
    print("=" * 70 + "\n")
    
    print("⏳ Waiting for authorization (or paste code manually if needed)...")
    
    # Simple wait
    import time
    timeout = 300
    start = datetime.now()
    
    while OAuthHandler.code is None:
        if (datetime.now() - start).seconds > timeout:
            print("❌ Timeout")
            server.shutdown()
            exit(1)
        time.sleep(0.5)
    
    print("✅ Code received!")
    server.shutdown()
    
    print("🔄 Exchanging code for tokens...")
    tokens = exchange_code_for_tokens(OAuthHandler.code)
    tokens['expires_at'] = datetime.now().timestamp() + tokens.get('expires_in', 3600)
    
    with open(YOUTUBE_TOKEN_FILE, 'w') as f:
        json.dump(tokens, f, indent=2)
    
    print("\n✅ SUCCESS! New token saved with upload permission.")
    print(f"   Refresh Token: {tokens.get('refresh_token', 'N/A')[:40]}...")

if __name__ == "__main__":
    main()
