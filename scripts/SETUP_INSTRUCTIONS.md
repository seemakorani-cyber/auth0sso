# Teams Transcript Downloader - Setup Instructions

## Overview

This tool downloads Teams meeting transcripts for the delivery-assessment skill. It uses browser-based authentication with MFA support.

## Prerequisites

- Python 3.7 or higher
- Windows, macOS, or Linux
- Teams account with calendar access
- Internet connection

## Setup Steps

### Step 1: Verify Python Installation

```bash
python --version
```

Should show Python 3.7 or higher. If not installed, download from https://www.python.org/

### Step 2: Install Dependencies

Navigate to the scripts directory:

```bash
cd scripts
pip install msal requests python-dotenv
```

Or use the batch file (Windows):
```bash
setup_teams.bat
```

### Step 3: Create .env File

Create a file named `.env` in the `scripts/` directory with Azure credentials:

```env
AZURE_CLIENT_ID=22cd99bd-a84b-4739-95cc-18a43f48acf1
AZURE_TENANT_ID=d508624f-a0b7-4fd3-9511-05b18ca02784
```

**Note:** These are the public client credentials for Teams authentication. They're already configured in `setup_teams.bat`.

### Step 4: Test the Setup

Run the downloader:

```bash
python download_teams_transcript.py --meeting-name "standup"
```

What happens:
1. A browser window opens
2. Sign in with your Teams account
3. If MFA is enabled, complete the MFA prompt
4. Browser closes automatically
5. Script downloads the meeting transcript
6. Saves to `PM-Automations/Recordings/[Meeting Name]_[Date].docx`

## Usage

### Command Line

```bash
python download_teams_transcript.py --meeting-name "Your Meeting Name"
```

Options:
- `--meeting-name` (required): Full or partial meeting name (case-insensitive)
- `--workspace` (optional): Custom workspace path
- `--clear-cache` (optional): Clear cached token and re-authenticate

### Windows Batch File (Easy)

Double-click: `download_transcript.bat`

Then:
1. Enter the meeting name when prompted
2. Browser opens for login
3. Transcript downloads automatically

### Multiple Transcripts

Just run the downloader multiple times with different meeting names. Token is cached for 1 hour, so you won't need to log in again.

## Token Caching

Tokens are cached locally for 1 hour in: `~/.teams_transcript_auth/token_cache.json`

- **First run:** Browser login required
- **Subsequent runs (within 1 hour):** Uses cached token (faster)
- **After 1 hour:** Browser login required again

To force re-authentication:
```bash
python download_teams_transcript.py --meeting-name "standup" --clear-cache
```

## Troubleshooting

### Browser Doesn't Open

**Solution:** Clear the MSAL cache:

```bash
rm -r ~/.msal_cache_directory
```

Then try again.

### "Access Denied" or "401 Unauthorized"

**Solution:** Clear the token cache:

```bash
rm ~/.teams_transcript_auth/token_cache.json
```

Then re-run and log in with correct credentials.

### Meeting Not Found

**Possible causes:**
- Meeting name doesn't match exactly (try partial name)
- Meeting is from more than 200 days ago
- Meeting doesn't have a recording yet

**Solution:** Try a shorter/different meeting name:

```bash
# Instead of:
python download_teams_transcript.py --meeting-name "Project XYZ Quarterly Review - Q2 Planning"

# Try:
python download_teams_transcript.py --meeting-name "standup"
```

### "No Transcript Found"

Teams generates transcripts automatically after meetings, but it can take several minutes. Try again in 5-10 minutes.

## Security Notes

✅ **Safe approaches:**
- Browser-based login (standard OAuth)
- Token cached locally with restricted permissions (600)
- Credentials stored in `.env` (in .gitignore)
- No passwords stored anywhere

❌ **Avoid:**
- Sharing the `.env` file
- Hardcoding passwords
- Using username/password auth (use browser instead)

## Integration with Delivery-Assessment Skill

After downloading the transcript:

1. Open Claude Code Desktop
2. Say: "delivery assessment"
3. Skill auto-discovers transcripts in `PM-Automations/Recordings/`
4. Generates Confluence report automatically

## File Structure

```
scripts/
├── download_teams_transcript.py   Main script
├── download_transcript.bat         Easy one-click (Windows)
├── setup_teams.bat                 Setup wizard (Windows)
├── teams_launcher.bat              Menu system (Windows)
├── requirements.txt                Python dependencies
├── .env                            Credentials (created during setup)
└── SETUP_INSTRUCTIONS.md          This file
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the error message carefully
3. Check that Python and dependencies are installed correctly
4. Verify `.env` file exists and has correct credentials

---

**Last Updated:** 2026-06-01
