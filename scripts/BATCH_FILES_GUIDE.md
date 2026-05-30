# Windows Batch Files Guide

Interactive batch files for easy Teams transcript downloading on Windows.

## Quick Start

### First Time: Run Setup
1. **Double-click** `setup_teams.bat`
2. Follow the prompts to create an Azure app
3. Enter your credentials when prompted
4. ✅ Setup complete!

### Download a Transcript
1. **Double-click** `download_transcript.bat`
2. Enter the Teams meeting name
3. ✅ Transcript auto-downloads to `Recordings/` folder
4. Run delivery-assessment skill in Claude Code

---

## Files Included

### 1. **teams_launcher.bat** ⭐ START HERE
Main menu with options:
- Download a transcript
- Setup (first-time)
- View documentation
- Exit

**Usage:** Double-click `teams_launcher.bat`

### 2. **setup_teams.bat** (First-time only)
Interactive setup wizard that:
- Checks Python installation
- Installs Python dependencies
- Guides Azure app registration
- Saves credentials to `.env`

**Usage:** Double-click, or select from launcher menu

**You only need to run this once!**

### 3. **download_transcript.bat** (Main workflow)
Downloads Teams transcripts with these features:
- Prompts for meeting name
- Auto-detects credentials
- Shows helpful error messages
- Saves to correct folder
- Displays next steps

**Usage:** Double-click whenever you need a transcript

---

## Detailed Usage

### Setup (One-Time)

```
1. Open Windows File Explorer
2. Navigate to: scripts\ folder
3. Double-click: setup_teams.bat
4. Follow on-screen instructions
   • Python check ✅
   • Install dependencies
   • Azure app registration guide
5. Enter Client ID and Tenant ID (from Azure)
6. Done! ✅
```

**What it does:**
- Verifies Python 3.7+ is installed
- Installs msal, requests, python-dotenv
- Runs `setup_teams_auth.py`
- Saves `.env` file with credentials

---

### Download Transcripts

```
1. Double-click: download_transcript.bat
2. Enter meeting name: "Project XYZ Standup"
3. Script searches Teams
4. Downloads latest transcript
5. Saves to Recordings\ folder ✅
6. Next: Run delivery-assessment in Claude Code
```

**Meeting name tips:**
- Use partial names: "standup" matches "Daily Team Standup"
- Case-insensitive: "SYNC", "sync", "Sync" all work
- Include keywords: "weekly", "planning", "retro"

---

### Using the Launcher Menu

```
1. Double-click: teams_launcher.bat
2. Choose option:
   [1] Download a transcript
   [2] Setup (first-time)
   [3] View documentation
   [4] Exit
3. Enter your choice and press Enter
```

**You can run this repeatedly** — the menu returns after each action, so you can download multiple transcripts in one session.

---

## Troubleshooting

### "Python is not installed"
**Solution:**
1. Install Python 3.7+ from https://www.python.org/
2. **Important:** Check "Add Python to PATH" during installation
3. Run `setup_teams.bat` again

### "No meetings found matching..."
**Solutions:**
- Try a shorter/partial name: `"standup"` instead of `"Daily Team Standup"`
- Meeting must be in your calendar (not just attendee)
- Name is case-insensitive

### "No transcript found for this meeting yet"
**Solution:**
- Teams takes 5-10 minutes after meeting ends to generate transcripts
- Wait a few minutes and run `download_transcript.bat` again

### ".env file not found after setup"
**Solutions:**
1. Make sure `setup_teams.bat` completed without errors
2. Check that `.env` file exists in `scripts\` folder
3. If missing, run `setup_teams.bat` again

### Authentication fails
**Solutions:**
1. Make sure Client ID and Tenant ID are correct
2. Check that API permissions are granted in Azure
3. Delete `~\.teams_transcript_cache.json` and try again
4. Run `setup_teams.bat` to re-enter credentials

---

## Batch File Details

### setup_teams.bat
```batch
1. Checks Python installation
2. Installs dependencies if needed
3. Runs setup_teams_auth.py
4. Creates .env file
5. Shows success/error messages
```

### download_transcript.bat
```batch
1. Checks .env file exists
2. Verifies Python installed
3. Prompts for meeting name
4. Runs Python script
5. Shows success/error messages
6. Displays next steps
```

### teams_launcher.bat
```batch
1. Shows main menu
2. Routes to appropriate batch file
3. Returns to menu after action
4. Allows repeated downloads in one session
```

---

## Environment Variables

The batch files automatically set:
- **WORKSPACE_PATH** — Where transcripts are saved (from `.env`)
- **PYTHON_PATH** — Python executable location

You can customize the workspace path in `scripts\.env`:
```
WORKSPACE_PATH=C:\Users\YourName\OneDrive - Royal Cyber Inc\Documents\PM-Automations
```

---

## Security Notes

✅ **Safe & Secure:**
- Credentials stored locally in `scripts\.env`
- OAuth login (Microsoft handles your password)
- No data sent to third parties
- Token cached locally for convenience

⚠️ **Keep `.env` private:**
- Contains your Azure credentials
- Don't share or commit to version control
- `.env` is in `.gitignore` (already excluded)

---

## Workflow Summary

```
┌─────────────────────────────────────────────┐
│  First Time: Run setup_teams.bat            │
│  (Creates Azure app, saves credentials)     │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  Download: Double-click download_transcript.bat    │
│  (Or use teams_launcher.bat for menu)       │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  Transcript saved to: Recordings\ folder    │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│  Open Claude Code Desktop                   │
│  Say: "delivery assessment"                 │
│  Skill auto-discovers transcript ✅         │
└─────────────────────────────────────────────┘
```

---

## Tips & Tricks

### Batch Download Multiple Meetings
1. Run `download_transcript.bat` multiple times
2. Enter different meeting names
3. All transcripts save to `Recordings\` folder
4. Run skill once — it processes all transcripts

### Keep Files for Reuse
- Question files: Stay in `Questions\` (reusable)
- Transcript files: Can be manually moved to `Processed\` after use

### View Saved Transcripts
Transcripts are saved with format:
```
[Meeting Name]_[Date]_[Time].docx
Example: Project_XYZ_Standup_20260530_090000.docx
```

View in `Recordings\` folder or via Python script output.

---

## Support

If you need help:
1. Check **Troubleshooting** section above
2. Review `TEAMS_TRANSCRIPT_SETUP.md` for detailed info
3. Check that credentials in `.env` are correct
4. Make sure workspace path is accessible
