#!/usr/bin/env python3
"""
Google Drive OAuth Setup Script (Headless / VPS friendly)
Mirip dengan youtube_oauth_setup.py

Flow:
1. Run this script to get Authorization URL
2. Open the URL in your browser
3. After authorization, copy the code
4. Run drive_oauth_exchange_code.py with the code

Scopes: drive + drive.file (read/write)
"""

import os
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

def load_env(path):
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")

load_env("/data/workspace/.env")

DRIVE_TOKEN_FILE = "/data/workspace/google_drive_tokens.json"
REDIRECT_URI = "http://localhost:8889"

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
]

CLIENT_ID = os.getenv("DRIVE_CLIENT_ID")
CLIENT_SECRET = os.getenv("DRIVE_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    print("ERROR: DRIVE_CLIENT_ID atau DRIVE_CLIENT_SECRET tidak ditemukan di .env")
    exit(1)

print("Client ID:", CLIENT_ID[:30] + "...")


class OAuthHandler(BaseHTTPRequestHandler):
    code = None

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)

        if "code" in query:
            OAuthHandler.code = query["code"][0]
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>Authorization Successful!</h1><p>You can close this tab.</p>")
        else:
            self.send_response(400)
            self.end_headers()

    def log_message(self, format, *args):
        pass


def get_auth_url():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
        "include_granted_scopes": "true",
    }
    return "https://accounts.google.com/o/oauth2/auth?" + urllib.parse.urlencode(params)


def main():
    print("=" * 70)
    print("Google Drive OAuth Setup (Read/Write)")
    print("=" * 70)
    print("Token akan disimpan ke:", DRIVE_TOKEN_FILE)

    if os.path.exists(DRIVE_TOKEN_FILE):
        print("WARNING: File sudah ada.")
        choice = input("Overwrite? (y/N): ").lower().strip()
        if choice != "y":
            print("Dibatalkan.")
            return
        print()

    auth_url = get_auth_url()

    print("[1/2] Buka URL berikut di browser:")
    print(auth_url)
    print("[2/2] Setelah authorize, copy code-nya, lalu jalankan:")
    print("python drive_oauth_exchange_code.py <code>")
    print("=" * 70)


if __name__ == "__main__":
    main()
