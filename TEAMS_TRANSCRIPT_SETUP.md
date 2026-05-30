# Teams Transcript Downloader Setup

Automatically download Teams meeting transcripts and feed them to the `delivery-assessment` skill.

## Overview

**Before:** Download transcript → Save to folder → Run skill  
**After:** `python download_teams_transcript.py --meeting-name "Meeting Name"` → Skill runs automatically

## What it does

1. ✅ Authenticates to your Teams account (OAuth)
2. ✅ Searches for a meeting by name
3. ✅ Downloads the latest transcript (.docx)
4. ✅ Saves to `Recordings/` folder automatically
5. ✅ Notifies you when ready for delivery-assessment skill

## Requirements

- **Python 3.7+** (check: `python --version`)
- **pip** (check: `pip --version`)
- **Azure account** with Teams access

## Initial Setup (One-time)

### 1. Install Python Dependencies

```bash
cd scripts
pip install -r requirements.txt
```

### 2. Create Azure App Registration

Run the interactive setup:

```bash
python setup_teams_auth.py
```

This will:
- Guide you through creating an Azure app in 5 minutes
- Save your credentials to `scripts/.env`

**Or manually** (if you prefer):

1. Go to https://portal.azure.com
2. Search **"App registrations"** → Click it
3. Click **"+ New registration"**
4. Name: `Teams Transcript Downloader`
5. Account types: **"Accounts in any organizational directory"**
6. Click **Register**

#### Add API Permissions

1. In your app → **API permissions**
2. Click **"+ Add a permission"**
3. Select **Microsoft Graph** → **Delegated permissions**
4. Search and add:
   - ✓ `OnlineMeetings.Read`
   - ✓ `OnlineMeetings.ReadWrite`
   - ✓ `Calendars.Read`
5. Click **"Grant admin consent"**

#### Copy Credentials

1. Go to **Overview** tab
2. Copy **Application (client) ID**
3. Go to **Directories + subscriptions** (top-right)
4. Copy **Directory (tenant) ID**

Copy these into `scripts/.env`:

```bash
AZURE_CLIENT_ID=your-client-id
AZURE_TENANT_ID=your-tenant-id
```

### 3. Configure Workspace Path (Windows Only)

Edit `scripts/.env`:

```bash
WORKSPACE_PATH=C:\Users\KrishnaKumar\OneDrive - Royal Cyber Inc\Documents\PM-Automations
```

On first run, it will create `Recordings/` if it doesn't exist.

## Usage

### Download a Transcript

```bash
python scripts/download_teams_transcript.py --meeting-name "Project XYZ Standup"
```

**Output:**
```
🔐 Authenticating to Teams...
🔍 Searching for meeting: 'Project XYZ Standup'...
Found meeting: Project XYZ Standup - Weekly
Start time: 2026-05-30T09:00:00Z
✅ Transcript saved to: C:\...\Recordings\Project_XYZ_Standup_20260530_090000.docx

Now run the delivery-assessment skill in Claude Code:
   Meeting name: Project XYZ Standup - Weekly
```

### Run Delivery Assessment

In **Claude Code**:

1. Say: **"delivery assessment"** or **"assess my team"**
2. The skill auto-discovers the transcript in `Recordings/`
3. It generates the Confluence-ready HTML report

---

## Troubleshooting

### "No meetings found matching..."

- Meeting name might be different — check your Teams calendar
- Try a shorter/partial name: `"standup"` instead of `"Daily Team Standup"`
- Ensure the meeting is in your calendar (not just an attendee)

### "No transcript found for this meeting yet"

Teams takes **5-10 minutes** after a meeting ends to generate transcripts.
- Wait a few minutes and try again
- Check the meeting ended (not still ongoing)

### "AZURE_CLIENT_ID and AZURE_TENANT_ID not set"

Run `python setup_teams_auth.py` to save credentials to `scripts/.env`

### Authentication fails / "Invalid credentials"

- Ensure your Client ID and Tenant ID are correct
- Make sure API permissions are granted (**Grant admin consent**)
- Try removing `~/.teams_transcript_cache.json` to force re-login

### Transcript not saving to Recordings folder

Check the `WORKSPACE_PATH` in `scripts/.env` is correct and accessible.

---

## How it works

```
User runs script
     ↓
Authenticate to Teams (OAuth)
     ↓
Search calendar for meeting by name
     ↓
Get latest recording
     ↓
Download transcript (.docx)
     ↓
Save to PM-Automations/Recordings/
     ↓
Ready for delivery-assessment skill
```

---

## Advanced Usage

### Batch Download Multiple Meetings

```bash
python scripts/download_teams_transcript.py --meeting-name "Standup"
python scripts/download_teams_transcript.py --meeting-name "Planning"
python scripts/download_teams_transcript.py --meeting-name "Retro"
```

Then run delivery-assessment once — it processes all transcripts.

### Custom Workspace Path

```bash
python scripts/download_teams_transcript.py \
  --meeting-name "Team Sync" \
  --workspace "D:\MyProjects\PM-Automations"
```

---

## Security

- ✅ **Credentials stored locally** — Never sent to third parties
- ✅ **OAuth login** — Microsoft handles your password (you never enter it here)
- ✅ **Token cache** — Saved to `~/.teams_transcript_cache.json` (encrypted by Windows)
- ✅ **No data forwarding** — Transcripts stay on your machine

---

## Support

If you hit issues:
1. Check the troubleshooting section above
2. Verify credentials in `scripts/.env`
3. Run `python setup_teams_auth.py` to re-enter credentials

