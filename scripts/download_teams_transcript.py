#!/usr/bin/env python3
"""
Download Teams meeting transcripts and save to delivery-assessment Recordings folder.

Usage:
    python download_teams_transcript.py --meeting-name "Project XYZ Standup"
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
from msal import PublicClientApplication

# Load environment variables
load_dotenv()

# Configuration
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
SCOPES = ["https://graph.microsoft.com/.default"]
GRAPH_API_BASE = "https://graph.microsoft.com/v1.0"

# Token cache file
CACHE_DIR = Path.home() / ".teams_transcript_auth"
CACHE_DIR.mkdir(exist_ok=True)
CACHE_FILE = CACHE_DIR / "token_cache.json"

# Workspace path
WORKSPACE = os.getenv("WORKSPACE_PATH") or str(Path.home() / "PM-Automations")
RECORDINGS_DIR = Path(WORKSPACE) / "Recordings"


def load_cached_token():
    """Load cached access token if it exists and is valid. Returns (token, refresh_token, expired)."""
    if not CACHE_FILE.exists():
        return None, None, False

    try:
        with open(CACHE_FILE, 'r') as f:
            cache_data = json.load(f)

        access_token = cache_data.get('access_token')
        refresh_token = cache_data.get('refresh_token')
        expires_at = datetime.fromisoformat(cache_data.get('expires_at', ''))

        is_expired = expires_at <= datetime.now()

        if access_token:
            return access_token, refresh_token, is_expired
    except (json.JSONDecodeError, ValueError, KeyError):
        pass

    return None, None, False


def save_token_to_cache(token, refresh_token, expires_in):
    """Save access token, refresh token, and expiration time to cache file."""
    try:
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        cache_data = {
            'access_token': token,
            'refresh_token': refresh_token,
            'expires_at': expires_at.isoformat(),
            'created_at': datetime.now().isoformat()
        }
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f)
        os.chmod(CACHE_FILE, 0o600)  # Secure file permissions
    except Exception as e:
        print(f"[WARNING] Could not save token cache: {e}")


def get_auth_token():
    """Authenticate using device flow (browser-based login with MFA support)."""

    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}"
    )

    # Try to use cached token first
    cached_token, refresh_token, is_expired = load_cached_token()

    if cached_token and not is_expired:
        print("[INFO] Using cached token (still valid)")
        return cached_token

    # Try to refresh expired token using refresh token
    if cached_token and is_expired and refresh_token:
        print("[INFO] Access token expired, refreshing...")
        try:
            token_response = app.acquire_token_by_refresh_token(refresh_token, scopes=SCOPES)
            if "access_token" in token_response:
                save_token_to_cache(
                    token_response["access_token"],
                    token_response.get("refresh_token", refresh_token),
                    token_response.get("expires_in", 3600)
                )
                print("[OK] Token refreshed. Cache updated.\n")
                return token_response["access_token"]
        except Exception as e:
            print(f"[INFO] Refresh failed ({str(e)}), will re-authenticate")

    # Full device flow login (first time or refresh failed)
    print("[INFO] Starting device flow login...\n")

    try:
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            raise Exception("Failed to initiate device flow")

        print(flow.get("message"))
        print()

        token_response = app.acquire_token_by_device_flow(flow)
    except Exception as e:
        raise Exception(f"Authentication failed: {str(e)}")

    if "access_token" not in token_response:
        error = token_response.get('error_description', 'Unknown error')
        raise Exception(f"Login failed: {error}")

    # Cache the token and refresh token
    save_token_to_cache(
        token_response["access_token"],
        token_response.get("refresh_token"),
        token_response.get("expires_in", 3600)
    )
    print("\n[OK] Login successful! Token cached for future use.\n")

    return token_response["access_token"]


def search_teams_meetings(token, meeting_name):
    """Search for Teams meetings by name and return matching events."""
    headers = {"Authorization": f"Bearer {token}"}

    # Fetch all recent events and filter client-side
    print("[INFO] Fetching recent events...")
    url = f"{GRAPH_API_BASE}/me/events"
    params = {"$top": "200"}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 401:
        raise Exception("Authentication token expired or invalid")

    if response.status_code != 200:
        raise Exception(f"Failed to fetch events: {response.status_code} - {response.text}")

    # Get all events
    events = response.json().get("value", [])

    if not events:
        print(f"[INFO] No events found in calendar")
        return []

    # Filter for matching meeting names (case-insensitive)
    matching_events = []
    for event in events:
        subject = event.get("subject", "").lower()
        if meeting_name.lower() in subject:
            matching_events.append(event)

    # Sort by start time (newest first)
    matching_events.sort(
        key=lambda e: e.get("start", {}).get("dateTime", ""),
        reverse=True
    )

    if not matching_events:
        print(f"[INFO] No meetings found matching '{meeting_name}'")
        print(f"[INFO] Searched {len(events)} events in your calendar")
        return []

    return matching_events


def get_meeting_transcript(token, meeting_id):
    """Get the transcript for a specific Teams meeting."""
    headers = {"Authorization": f"Bearer {token}"}

    # Get meeting details and check for recordings
    url = f"{GRAPH_API_BASE}/me/onlineMeetings/{meeting_id}/recordings"
    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        # Try alternate endpoint
        url = f"{GRAPH_API_BASE}/me/calendarEvents/{meeting_id}/instances"
        response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    recordings = response.json().get("value", [])
    if not recordings:
        return None

    # Get the latest recording's transcript
    latest = recordings[0]

    # Check for transcript in recording
    if "transcripts" in latest:
        for transcript in latest.get("transcripts", []):
            transcript_url = transcript.get("contentUrl")
            if transcript_url:
                return download_transcript_file(token, transcript_url)

    return None


def download_transcript_file(token, url):
    """Download transcript file from URL."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content


def find_latest_meeting_recording(token, meeting_name):
    """Find latest meeting and download its transcript."""
    meetings = search_teams_meetings(token, meeting_name)

    if not meetings:
        return None

    latest_meeting = meetings[0]
    meeting_id = latest_meeting["id"]
    subject = latest_meeting["subject"]
    start_time = latest_meeting["start"]["dateTime"]

    print(f"[OK] Found meeting: {subject}")
    print(f"[INFO] Start time: {start_time}")

    # Attempt to get transcript
    transcript_content = get_meeting_transcript(token, meeting_id)

    if not transcript_content:
        print("[WARNING] No transcript found for this meeting yet.")
        print("[INFO] Teams may take a few minutes to generate transcripts after the meeting ends.")
        return None

    return {
        "subject": subject,
        "start_time": start_time,
        "content": transcript_content
    }


def save_transcript(transcript_data):
    """Save transcript to Recordings folder."""
    if not transcript_data:
        return None

    # Create Recordings directory if it doesn't exist
    RECORDINGS_DIR.mkdir(parents=True, exist_ok=True)

    # Generate filename from meeting name and timestamp
    subject = transcript_data["subject"]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Sanitize filename
    safe_subject = "".join(c for c in subject if c.isalnum() or c in (" ", "-", "_")).rstrip()
    filename = f"{safe_subject}_{timestamp}.docx"

    filepath = RECORDINGS_DIR / filename

    # Save file
    with open(filepath, "wb") as f:
        f.write(transcript_data["content"])

    return filepath


def main():
    parser = argparse.ArgumentParser(
        description="Download Teams meeting transcript to delivery-assessment Recordings folder"
    )
    parser.add_argument(
        "--meeting-name",
        required=True,
        help="Name or partial name of the Teams meeting to download"
    )
    parser.add_argument(
        "--workspace",
        help=f"Custom workspace path (default: {WORKSPACE})"
    )
    parser.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear cached login and force re-authentication"
    )

    args = parser.parse_args()

    # Validate environment
    if not CLIENT_ID or not TENANT_ID:
        print("[ERROR] AZURE_CLIENT_ID and AZURE_TENANT_ID not set in .env")
        print("[INFO] Run setup_teams.bat to configure credentials")
        sys.exit(1)

    # Clear cache if requested
    if args.clear_cache:
        if CACHE_FILE.exists():
            CACHE_FILE.unlink()
            print("[OK] Cache cleared. You'll need to login next time.\n")

    try:
        print("[INFO] Authenticating to Teams...")
        token = get_auth_token()

        print(f"[INFO] Searching for meeting: '{args.meeting_name}'...")
        transcript_data = find_latest_meeting_recording(token, args.meeting_name)

        if transcript_data:
            filepath = save_transcript(transcript_data)
            print(f"[OK] Transcript saved to: {filepath}")
            print(f"\n[INFO] Next: Open Claude Code and say 'delivery assessment'")
        else:
            print("[ERROR] Failed to download transcript")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n[INFO] Cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
