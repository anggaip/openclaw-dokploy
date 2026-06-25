import os, json, urllib.request, urllib.parse
from datetime import datetime

def load_env(path):
    if os.path.exists(path):
        with open(path) as f:\n            for line in f:\n                line = line.strip()\n                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")

load_env('/data/workspace/.env')

CLIENT_ID = os.getenv('YOUTUBE_CLIENT_ID')
CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')

if not CLIENT_ID or not CLIENT_SECRET:
    print("❌ ERROR: YOUTUBE_CLIENT_ID or YOUTUBE_CLIENT_SECRET not found in .env")
    exit(1)

code = "4/0AdkVLPymaZzFoWFxErF7TBHwmCbSe_2Rxme1D-nQh5ES_OLpUPVLmxyDvy4c54grjZ8zQQ"

data = {
    "code": code,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "redirect_uri": "http://localhost:8888",
    "grant_type": "authorization_code"
}

req = urllib.request.Request(
    "https://oauth2.googleapis.com/token",
    data=urllib.parse.urlencode(data).encode(),
    headers={"Content-Type": "application/x-www-form-urlencoded"}
)

response = urllib.request.urlopen(req, timeout=15)
tokens = json.loads(response.read().decode())
tokens["expires_at"] = datetime.now().timestamp() + tokens.get("expires_in", 3600)
json.dump(tokens, open("/data/workspace/youtube_tokens.json", "w"), indent=2)
print("✅ SUCCESS! youtube_tokens.json saved")
print("Refresh token:", tokens.get("refresh_token", "N/A")[:60] + "...")
