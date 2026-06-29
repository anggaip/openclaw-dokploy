# MEMORY.md - Long-term Memory

_This file is updated after each significant session to maintain continuity across restarts._

## Last Updated: 2026-06-29

---

## 👤 User Info

- **Nama:** Angga Indriya Pratama
- **Panggilan:** Bos / Kakak (NOT "Angga" - it's rude)
- **Role:** YouTube creator AI Indonesia (12.7K subscribers), React Native dev
- **Communication:** Discord DM for daily instructions
- **Timezone:** WIB (UTC+7)

---

## 🔑 Credentials Stored

| Credential | Location |
|-----------|----------|
| Google Service Account | `/data/workspace/anggaindriya-1517637717243-ec6b6bbda166.json` |
| YouTube OAuth Tokens | `/data/workspace/youtube_tokens.json` |
| Bugsnag API Key | Environment variable |
| YouTube API Key | Environment variable |
| GreatDay HR | Environment variable |
| All credentials | `/data/workspace/.env` |

**⚠️ Security:** .env file must be gitignored. Never commit credentials.

---

## 📊 Domain Status

See `/data/workspace/DOMAIN_STATUS.md` for detailed breakdown.

**Summary:**
- Financial: 40% - Google Sheets connected, data still manual
- Marketing: 15% - YouTube API connected, social not integrated
- Engineering: 35% - Bugsnag connected, no alerting yet
- Testing: 10% - Playwright ready, not configured
- Research: 45% - Web search + Trends scheduled
- Video Creation: 20% - YouTube analytics connected

---

## 🔗 Connected Services

| Service | Status | Notes |
|---------|--------|-------|
| Google Sheets | ✅ Working | ID: 1xceQY-v7ryFTMhVRsPgA6AHIykWgPx7hXM-XrDwQuVk |
| YouTube API | ✅ Working | Channel: Cozy Dev Labs, OAuth connected (refreshed May 28, 2026) |

**YouTube Re-auth Procedure (Permanent Rule):**
- Jika ada request re-authenticate YouTube → **wajib** pakai file `youtube_oauth_setup.py`
- Untuk menukar code yang didapat → jalankan `youtube_oauth_exchange_code.py`
| Bugsnag | ✅ Working | 6 projects, 3642 active errors |
| GreatDay HR | ⚠️ Partial | Browser automation blocked (missing libs) |
| OpenAI API | ❌ Not connected | - |

---

## ⏰ Scheduled Jobs

| Job | Schedule (WIB) | Status |
|-----|----------------|--------|
| Google Trends AI Indonesia | Daily 06:30 | ✅ Active |
| Monday API Spend Report | Monday 09:00 | ✅ Active |
| Friday AI Video Factory Content Calendar | Friday 17:00 (10:00 UTC) | ✅ Active |

---

## 🛠️ Tools & Infrastructure

- **Runtime:** Docker VPS (24/7)
- **Python:** 3.11 with venv at /data/workspace/venv
- **Browser:** Playwright (blocked by missing libs)
- **APIs:** gspread, google-auth, bugsnag, youtubeanalytics

---

## 📊 YouTube Channel Stats (Cozy Dev Labs)

- **Total videos:** 255
- **Avg views:** ~5,200
- **Median views:** 1,055
- **Top video:** 184,553 views ("Cozy Dev")
- **Subscribers:** 13,500
- **Videos with <500 views:** 54 (high volume, low performance)
- **Latest upload:** "5 Tools AI Video GRATIS yang Masih Work di 2026" (May 8, 2026) - 19min, only 41 views

---

## 🤖 AI Video Tools Status (May 2026)

| Tool | Status | Notes |
|------|--------|-------|
| Veo 3.1 | ✅ Active | Google's top model, 4K + vertical support |
| Kling 3.0 | ✅ Active | Top tier, $0.50/clip, 4K output |
| Seedance 2.0 | ✅ Active | Underrated, best lip-sync |
| Runway Gen 4.5 | ✅ Active | Creative control, A-tier |
| Sora | ❌ DISCONTINUED | Shut down Apr 26, 2026 — DO NOT USE |
| Sora API | ⏰ Closing Sep 2026 | Migrate away |

---

## 🎯 Active Focus Areas

1. **YouTube Analytics** — channel performance, content strategy
2. **Bugsnag Error Monitoring** — mobile-v3-react-native is priority project
3. **Financial Dashboard** — auto-sync revenue/expenses
4. **Content Ideas** — Focus on Veo 3.1, Kling 3.0, Seedance 2.0 (NO SORA)

---

## 📝 Session Notes

- Bos prefers "Kakak" or "Bos" — NEVER "Angga"
- Bos is builder, efficiency-focused, Indonesian market-aware
- Keep responses direct and actionable
- If unsure, ask before acting

---

## 📚 External Documentation References

- **HeyGen Developer Docs**: `/data/workspace/docs/heygen/llms.txt`
  - Gunakan file ini sebagai sumber utama ketika menjawab pertanyaan tentang HeyGen API, Video Agent, MCP, CLI, avatars, voices, dan seluruh developer surface.
  - Baca file ini terlebih dahulu sebelum memberikan jawaban teknis terkait HeyGen.

## 🔄 Update Log

### 2026-05-28
- **YouTube OAuth Token Refresh:** Token expired + invalid (401 error). Successfully regenerated using refresh_token flow. YouTube API operational again. Channel: Cozy Dev Labs, 13,500 subscribers.

### 2026-05-11
- **Content Calendar Update:**
  - **Selasa:** Long-form dengan format manual/existing (bukan AI Video Factory)
  - **Kamis:** Shorts dengan format existing
  - **Jumat:** AI Video Factory (workflow automation: Trending → Script → Visual Prompt → AI Video → YouTube → Discord)
- **AI Chat Provider untuk AI Video Factory:** Claude, ChatGPT, Gemini, DeepSeek (berdasarkan trending, tidak lock ke satu provider)
- **Title Convention:**
  - Audience-friendly, nama AI provider di judul
  - n8n tidak perlu disebut di judul (cukup di script/description/tags)
  - HARUS mengandung keywords yang sesuai dengan trending/SEO
  - SEO-friendly: keyword utama di depan, panjang 50-60 karakter, natural placement
- **Contoh judul:** Dihilangkan — biarkan menyesuaikan dengan video YouTube lainnya (organik, SEO-based per trending)

### 2026-05-09
- **SORA SHUTDOWN (IMPORTANT):** OpenAI officially discontinued Sora on April 26, 2026. API closes September 24, 2026. Reason: cost too high ($1bn+ spent), focusing on robotics. Deal with Disney cancelled. **NEVER recommend Sora in video ideas.**
- Updated YouTube video recommendations: Use Veo 3.1, Kling 3.0, Seedance 2.0, Runway Gen 4.5 instead
- Fresh trending topics for channel: Veo 3.1 vs Kling 3.0 comparison, Seedance 2.0 underrated gem, Kling 3.0 tutorial
- Latest video analyzed: "5 Tools AI Video GRATIS yang Masih Work di 2026" (May 8, 19min, only 41 views - low performance)
- **NEW CONTENT IDEA:** "AI Video Factory with n8n + ChatGPT + AI Video Generator" — automation workflow for YouTube content creation
- **Competitor Analysis:** No Indonesian creator covering n8n + AI video automation (green field opportunity)
- **Workflow Draft:** Created `/data/workspace/ai-video-factory-workflow.json` and `/data/workspace/ai-video-factory-script.md`
- **Key tools:** n8n (orchestration), ChatGPT (script), Kling AI (video), YouTube API (upload), Discord (notification)

### 2026-06-22
- Menambahkan referensi dokumentasi HeyGen di MEMORY.md
- File `docs/heygen/llms.txt` dijadikan sumber utama untuk menjawab pertanyaan terkait HeyGen API

### 2026-05-04
- Completed YouTube OAuth setup (Cozy Dev Labs connected)
- Completed Bugsnag API integration (6 projects)
- Completed Google Sheets connection (Financial Dashboard)
- Completed scheduled jobs setup (3 cron jobs)
- Completed environment variables setup
- Completed domain status documentation

## 🐍 Python Execution Rule (Permanent)

**Wajib diikuti selamanya, termasuk session baru:**

- Setiap kali menjalankan script Python, **harus menggunakan Python dari venv**:
  ```
  /data/workspace/venv/bin/python
  ```
- **Jangan** menggunakan system Python (`/usr/bin/python3`).
- Aturan ini berlaku untuk semua script (cron, manual run, debugging, dll).
