# MEMORY.md - Long-term Memory

## Google / YouTube Credentials
- Semua credential Google/YouTube diambil dari file `/data/workspace/.env`
- Variabel penting:
  - `YOUTUBE_API_KEY`
  - `YOUTUBE_CLIENT_ID`
  - `YOUTUBE_CLIENT_SECRET`
  - `GOOGLE_APPLICATION_CREDENTIALS` → `/data/workspace/anggaindriya-1517637717243-ec6b6bbda166.json`

Catatan: Jangan menyimpan nilai rahasia secara langsung di file ini. Selalu referensi ke `.env`.

## Python Environment
- Virtual Environment utama: `/data/workspace/venv/bin/python`
- Selalu gunakan venv ini untuk menjalankan script Python yang membutuhkan library Google/YouTube

## YouTube Channel Data
- Saat diminta data channel YouTube terbaru (subscriber, video, performa, dll), **selalu gunakan script**:
  `/data/workspace/test_youtube_token.py`
- Jangan buat script baru kecuali diminta explicitly.

## Development Rules
- Sebelum membuat script atau file baru, **harus konfirmasi dulu**.
- Jangan langsung membuat file/script tanpa sepengetahuan Bos.

---
Dibuat: 2026-06-23 | Update: 2026-07-02
