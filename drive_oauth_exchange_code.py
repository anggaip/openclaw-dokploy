#!/usr/bin/env python3
"""
Google Drive OAuth - Exchange Authorization Code
Companion script untuk drive_oauth_setup.py

Usage:
    python drive_oauth_exchange_code.py <authorization_code>
"""

import os
import sys
import json
import urllib.request
import urllib.parse
from datetime import datetime

def load_env(path):
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")

load_env('/data/workspace/.env')

DRIVE_TOKEN_FILE = "/data/workspace/google_drive_tokens.json"

CLIENT_ID = os.getenv("DRIVE_CLIENT_ID")
CLIENT_SECRET = os.getenv("DRIVE_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8889"

if not CLIENT_ID or not CLIENT_SECRET:
    print("❌ ERROR: DRIVE_CLIENT_ID atau DRIVE_CLIENT_SECRET tidak ditemukan di .env")
    sys.exit(1)

def exchange_code(code):
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

    with urllib.request.urlopen(req, timeout=20) as response:
        return json.loads(response.read().decode())

def save_tokens(token_data):
    token_data['client_id'] = CLIENT_ID
    token_data['client_secret'] = CLIENT_SECRET
    token_data['token_uri'] = 'https://oauth2.googleapis.com/token'
    token_data['scopes'] = [
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.file',
    ]

    with open(DRIVE_TOKEN_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)
        
    print(f"\n✅ Token berhasil disimpan ke {DRIVE_TOKEN_FILE}")
    print(f"   Access token expires in: {token_data.get('expires_in', 'N/A')} seconds")

def main():
    if len(sys.argv) < 2:
        print("Usage: python drive_oauth_exchange_code.py <authorization_code>")
        sys.exit(1)

    code = sys.argv[1].strip()

    print("=" * 60)
    print("Exchanging authorization code for Google Drive tokens...")
    print("=" * 60)

    try:
        token_data = exchange_code(code)
        save_tokens(token_data)
        print("\n🎉 Google Drive OAuth berhasil!")
        print("   Token sekarang bisa digunakan untuk akses Drive.")
    except Exception as e:
        print(f"\n❌ Gagal exchange code: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
