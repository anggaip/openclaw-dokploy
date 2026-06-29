#!/usr/bin/env python3
"""
Google Drive Upload Utility
Fungsi untuk upload file ke Google Drive dengan mudah.

Usage:
    from drive_upload import upload_to_drive

    upload_to_drive(
        file_path="/path/to/video.mp4",
        folder_id="19pKlyB5LngsmrJo8p0O7sfBdRzT-NnoF",  # Reels folder
        file_name="Tips AI Video 2026.mp4"
    )
"""

import os
import json
import mimetypes
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError


DRIVE_TOKEN_FILE = "/data/workspace/google_drive_tokens.json"


def get_drive_service():
    """Load credentials and return Drive service."""
    if not os.path.exists(DRIVE_TOKEN_FILE):
        raise FileNotFoundError(f"Token file not found: {DRIVE_TOKEN_FILE}")

    creds = Credentials.from_authorized_user_info(
        json.load(open(DRIVE_TOKEN_FILE))
    )
    return build('drive', 'v3', credentials=creds)


def upload_to_drive(file_path, folder_id, file_name=None):
    """
    Upload file ke Google Drive.

    Args:
        file_path: Path file yang akan diupload
        folder_id: ID folder tujuan di Drive
        file_name: Nama file di Drive (opsional, default pakai nama asli)

    Returns:
        dict: Metadata file yang diupload (id, name, webViewLink)
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    service = get_drive_service()

    if file_name is None:
        file_name = os.path.basename(file_path)

    # Deteksi mime type
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'

    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }

    media = MediaFileUpload(
        file_path,
        mimetype=mime_type,
        resumable=True
    )

    try:
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, webViewLink, mimeType, size'
        ).execute()

        print(f"✅ Upload berhasil: {uploaded_file['name']}")
        print(f"   ID: {uploaded_file['id']}")
        print(f"   Link: {uploaded_file['webViewLink']}")

        return uploaded_file

    except HttpError as error:
        print(f"❌ Upload gagal: {error}")
        raise


def upload_to_reels(file_path, file_name=None):
    """
    Shortcut untuk upload langsung ke folder Reels.
    """
    REELS_FOLDER_ID = "19pKlyB5LngsmrJo8p0O7sfBdRzT-NnoF"
    return upload_to_drive(file_path, REELS_FOLDER_ID, file_name)


if __name__ == "__main__":
    # Contoh penggunaan
    print("Google Drive Upload Utility")
    print("Contoh: upload_to_reels('/path/to/video.mp4')")
