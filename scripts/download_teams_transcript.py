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
from msal import PublicClientApplication, ConfidentialClientApplication

# Load environment variables
load_dotenv()

# Configuration
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")  # For confidential clients
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
    """Load cached access token if it exists and is valid."""
    if not CACHE_FILE.exists():
        return None

    try:
        with open(CACHE_FILE, 'r') as f:
            cache_data = json.load(f)

        # Check if token exists and hasn't expired
        if 'access_token' in cache_data:
            expires_at = datetime.fromisoformat(cache_data.get('expires_at', ''))
            if expires_at > datetime.now():
                return cache_data['access_token']
    except (json.JSONDecodeError, ValueError, KeyError):
        pass

    return None


def save_token_to_cache(token, expires_in):
    """Save access token and expiration time to cache file."""
    try:
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        cache_data = {
            'access_token': token,
            'expires_at': expires_at.isoformat(),
            'created_at': datetime.now().isoformat()
        }
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f)
        os.chmod(CACHE_FILE, 0o600)  # Secure file permissions
    except Exception as e:
        print(f"[WARNING] Could not save token cache: {e}")


def get_auth_token_confidential():
    """Get token for confidential client (using client secret)."""
    app = ConfidentialClientApplication(
        client_id=CLIENT_ID,
        client_credential=CLIENT_SECRET,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}"
    )

    print("[INFO] Authenticating with client credentials...")
    token_response = app.acquire_token_for_client(scopes=SCOPES)

    if "access_token" not in token_response:
        error = token_response.get('error_description', 'Unknown error')
        raise Exception(f"Authentication failed: {error}")

    save_token_to_cache(token_response["access_token"], token_response.get("expires_in", 3600))
    print("[OK] Authentication successful!")

    return token_response["access_token"]


def get_auth_token_public():
    """Get token for public client (using device flow)."""
    # Try to use cached token first
    cached_token = load_cached_token()
    if cached_token:
        print("[INFO] Using cached login (valid for ~1 hour)")
        return cached_token

    print("[INFO] No valid cached token. Logging in...")

    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}"
    )

    # Try to get token from MSAL cache
    accounts = app.get_accounts()
    if accounts:
        token_response = app.acquire_token_silent(SCOPES, account=accounts[0])
        if token_response and "access_token" in token_response:
            save_token_to_cache(token_response["access_token"], token_response.get("expires_in", 3600))
            return token_response["access_token"]

    # Device flow login
    print("[INFO] Opening browser for Teams login...")
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise Exception("Failed to initiate device flow")

    print(f"\n[ACTION] Enter this code: {flow['user_code']}")
    print(f"[ACTION] Go to: https://microsoft.com/devicelogin\n")

    token_response = app.acquire_token_by_device_flow(flow)
    if "access_token" not in token_response:
        error = token_response.get('error_description', 'Unknown error')
        raise Exception(f"Login failed: {error}")

    # Cache the token
    save_token_to_cache(token_response["access_token"], token_response.get("expires_in", 3600))
    print("[OK] Login successful! Token cached for next time.\n")

    return token_response["access_token"]


def get_auth_token():
    """Get authentication token - uses client secret if available, otherwise device flow."""
    if CLIENT_SECRET:
        return get_auth_token_confidential()
    else:
        return get_auth_token_public()


def search_teams_meetings(token, meeting_name):
    """Search for Teams meetings by name and return matching events."""
    headers = {"Authorization": f"Bearer {token}"}

    # Escape single quotes for OData filter
    escaped_name = meeting_name.replace("'", "''")

    # Search for calendar events containing the meeting name
    filter_query = f"contains(subject, '{escaped_name}')"
    url = f"{GRAPH_API_BASE}/me/calendarview"
    params = {
        "$filter": filter_query,
        "$orderby": "start/dateTime desc",
        "$top": "10"
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 401:
        raise Exception("Authentication token expired or invalid")

    if response.status_code == 400:
        # Try without filter if special characters cause issues
        print("[INFO] Retrying search without special character handling...")
        response = requests.get(
            f"{GRAPH_API_BASE}/me/calendarview",
            headers=headers,
            params={
                "$orderby": "start/dateTime desc",
                "$top": "50"
            }
        )
        if response.status_code != 200:
            response.raise_for_status()

        # Filter manually on the client side
        events = response.json().get("value", [])
        matching_events = [e for e in events if meeting_name.lower() in e.get("subject", "").lower()]

        if not matching_events:
            print(f"[INFO] No meetings found matching '{meeting_name}'")
            return []

        return matching_events

    response.raise_for_status()

    events = response.json().get("value", [])
    if not events:
        print(f"[INFO] No meetings found matching '{meeting_name}'")
        return []

    return events


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
