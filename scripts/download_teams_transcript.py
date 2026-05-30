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
from datetime import datetime
from dotenv import load_dotenv
from msal import PublicClientApplication
from urllib.parse import urljoin

# Load environment variables
load_dotenv()

# Configuration
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
SCOPES = ["https://graph.microsoft.com/.default"]
GRAPH_API_BASE = "https://graph.microsoft.com/v1.0"
CACHE_FILE = Path.home() / ".teams_transcript_cache.json"

# Workspace path (maps to delivery-assessment Recordings folder)
# On Windows: C:\Users\KrishnaKumar\OneDrive - Royal Cyber Inc\Documents\PM-Automations
WORKSPACE = os.getenv("WORKSPACE_PATH") or str(Path.home() / "PM-Automations")
RECORDINGS_DIR = Path(WORKSPACE) / "Recordings"


def get_auth_token():
    """Authenticate and return access token using MSAL."""
    app = PublicClientApplication(
        client_id=CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{TENANT_ID}"
    )

    # Try to get token from cache
    accounts = app.get_accounts()
    if accounts:
        token_response = app.acquire_token_silent(SCOPES, account=accounts[0])
        if token_response and "access_token" in token_response:
            return token_response["access_token"]

    # Interactive login
    print("Opening browser for Teams login...")
    flow = app.initiate_device_flow(scopes=SCOPES)
    if "user_code" not in flow:
        raise Exception("Failed to initiate device flow")

    print(f"\nEnter this code: {flow['user_code']}")
    print("in your browser at: https://microsoft.com/devicelogin\n")

    token_response = app.acquire_token_by_device_flow(flow)
    if "access_token" not in token_response:
        raise Exception(f"Failed to get token: {token_response.get('error_description', 'Unknown error')}")

    return token_response["access_token"]


def search_teams_meetings(token, meeting_name):
    """Search for Teams meetings by name and return matching events."""
    headers = {"Authorization": f"Bearer {token}"}

    # Search for calendar events containing the meeting name
    filter_query = f"contains(subject, '{meeting_name}')"
    url = f"{GRAPH_API_BASE}/me/calendarview?$filter={filter_query}&$orderby=start/dateTime desc&$top=10"

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    events = response.json().get("value", [])
    if not events:
        print(f"No meetings found matching '{meeting_name}'")
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

    print(f"Found meeting: {subject}")
    print(f"Start time: {start_time}")

    # Attempt to get transcript
    transcript_content = get_meeting_transcript(token, meeting_id)

    if not transcript_content:
        print("⚠️  No transcript found for this meeting yet.")
        print("Note: Teams may take a few minutes to generate transcripts after the meeting ends.")
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

    args = parser.parse_args()

    # Validate environment
    if not CLIENT_ID or not TENANT_ID:
        print("❌ Error: AZURE_CLIENT_ID and AZURE_TENANT_ID not set")
        print("Run: python scripts/setup_teams_auth.py")
        sys.exit(1)

    try:
        print("🔐 Authenticating to Teams...")
        token = get_auth_token()

        print(f"🔍 Searching for meeting: '{args.meeting_name}'...")
        transcript_data = find_latest_meeting_recording(token, args.meeting_name)

        if transcript_data:
            filepath = save_transcript(transcript_data)
            print(f"✅ Transcript saved to: {filepath}")
            print(f"\nNow run the delivery-assessment skill in Claude Code:")
            print(f"   Meeting name: {transcript_data['subject']}")
        else:
            print("❌ Failed to download transcript")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n⚠️  Cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
