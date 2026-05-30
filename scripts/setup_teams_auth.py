#!/usr/bin/env python3
"""
Setup Azure app registration for Teams transcript download.
Run this once to configure credentials.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

SCRIPT_DIR = Path(__file__).parent
ENV_FILE = SCRIPT_DIR / ".env"


def setup_azure_app():
    """Guide user through Azure app registration."""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║         Teams Transcript Downloader - Azure Setup                 ║
╚════════════════════════════════════════════════════════════════════╝

To download Teams meeting transcripts, you need to register an Azure app.
This is a one-time setup (takes ~5 minutes).

STEP 1: Create Azure App Registration
─────────────────────────────────────

1. Go to: https://portal.azure.com
2. Search for "App registrations" and click it
3. Click "+ New registration"
4. Fill in:
   - Name: "Teams Transcript Downloader"
   - Supported account types: "Accounts in any organizational directory (Any Azure AD + personal Microsoft)"
5. Click "Register"

STEP 2: Add API Permissions
────────────────────────────

1. In the app, go to "API permissions"
2. Click "+ Add a permission"
3. Click "Microsoft Graph"
4. Click "Delegated permissions"
5. Search and select these permissions:
   ✓ OnlineMeetings.Read
   ✓ OnlineMeetings.ReadWrite
   ✓ Calendars.Read
6. Click "Add permissions"
7. Click "Grant admin consent for [Your Org]"

STEP 3: Copy Your Credentials
──────────────────────────────

1. Go to "Overview" tab
2. Copy: Application (client) ID
3. Go to "Directories + subscriptions" (top right)
4. Copy: Directory (tenant) ID

STEP 4: Enter Credentials Below
────────────────────────────────
""")

    client_id = input("Enter Application (client) ID: ").strip()
    tenant_id = input("Enter Directory (tenant) ID: ").strip()
    workspace = input("Enter workspace path (or press Enter for default): ").strip()

    if not client_id or not tenant_id:
        print("❌ Error: Client ID and Tenant ID are required")
        sys.exit(1)

    # Save to .env file
    env_content = f"""# Azure credentials for Teams transcript download
AZURE_CLIENT_ID={client_id}
AZURE_TENANT_ID={tenant_id}
{"WORKSPACE_PATH=" + workspace if workspace else "# WORKSPACE_PATH=C:\\\\Users\\\\Your\\\\Path"}
"""

    with open(ENV_FILE, "w") as f:
        f.write(env_content)

    print(f"\n✅ Credentials saved to: {ENV_FILE}")
    print("\nYou can now run:")
    print("  python scripts/download_teams_transcript.py --meeting-name \"Your Meeting Name\"")


if __name__ == "__main__":
    # Check if .env already exists
    if ENV_FILE.exists():
        overwrite = input(f"{ENV_FILE} already exists. Overwrite? (y/n): ").lower()
        if overwrite != "y":
            print("Setup cancelled")
            sys.exit(0)

    setup_azure_app()
