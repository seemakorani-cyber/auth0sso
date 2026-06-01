# Email to Admin: Teams Transcript Downloader - Browser-Based Authentication Testing

---

**Subject:** Testing Teams Transcript Downloader - Browser-Based Login (MFA-Compatible)

Dear Admin,

We've developed a Teams Transcript Downloader tool to automate downloading meeting transcripts for our delivery assessment process. We need your help testing the browser-based authentication approach.

## What This Does

This tool allows users to:
1. Double-click a batch file → Enter meeting name → Get transcript automatically
2. Integrates with our delivery-assessment skill for automated reporting

## Authentication Approach (Browser-Based - MFA Compatible)

**How it works:**
- User runs the downloader
- A browser window opens for Teams login
- User logs in normally (MFA prompts work natively)
- Script gets access token and downloads transcript
- Token cached for 1 hour (no re-login needed)

**Why this approach:**
✅ Supports Multi-Factor Authentication (MFA)  
✅ Secure (no passwords stored)  
✅ Standard OAuth flow (Microsoft recommended)  
✅ User-friendly (browser login feels natural)  

## Quick Test (5 minutes)

### Prerequisites
- Python 3.7+ installed and in PATH
- Git repository cloned: `seemakorani-cyber/auth0sso`

### Test Steps

1. **Checkout the branch:**
   ```bash
   git fetch origin claude/sleepy-carson-d4d3t
   git checkout claude/sleepy-carson-d4d3t
   cd scripts
   ```

2. **Set up (first time only):**
   
   **Option A - Batch file (Windows):**
   ```bash
   setup_teams.bat
   ```
   
   **Option B - Manual:**
   ```bash
   pip install msal requests python-dotenv
   # Create .env file in scripts/ with:
   # AZURE_CLIENT_ID=22cd99bd-a84b-4739-95cc-18a43f48acf1
   # AZURE_TENANT_ID=d508624f-a0b7-4fd3-9511-05b18ca02784
   ```

3. **Run the downloader:**
   ```bash
   python download_teams_transcript.py --meeting-name "standup"
   ```

4. **Expected behavior:**
   - Browser opens → Teams login page appears
   - You log in (MFA works if enabled)
   - Browser closes automatically
   - Script downloads transcript to `PM-Automations/Recordings/`
   
5. **Test token caching:**
   - Run the command again
   - Should complete faster (uses cached token)
   - Delete `~/.teams_transcript_auth/token_cache.json` to force re-login

## What We Need From You

Please test and confirm:

- [ ] Browser opens correctly for Teams login
- [ ] Your MFA works (if enabled)
- [ ] Script downloads transcript successfully
- [ ] Token caching works (run twice - second should be faster)
- [ ] Transcript saves to `PM-Automations/Recordings/` folder
- [ ] Test with a partial meeting name (e.g., "standup" finds "Daily Standup")

## Potential Issues & Solutions

| Issue | Solution |
|-------|----------|
| "AADSTS7000218: client_secret required" | ❌ Old issue, fixed with browser auth |
| Browser doesn't open | Check if MSAL cache needs clearing |
| "Access Denied" on transcript download | Check if meeting actually has transcript |
| Token cache not working | Delete `~/.teams_transcript_auth/token_cache.json` |

## Files to Review

- `scripts/download_teams_transcript.py` — Main Python script
- `scripts/download_transcript.bat` — Windows batch file (easy one-click)
- `scripts/setup_teams.bat` — Setup wizard for users
- `scripts/requirements.txt` — Dependencies (msal, requests, python-dotenv)

## Next Steps After Testing

Once confirmed working:
1. We'll add setup instructions to the repo README
2. Deploy to production branch
3. Distribute batch files to team for easy access

## Questions?

Please reply with:
- ✅ What worked
- ❌ What failed
- 💡 Any suggestions for improvement
- 🐛 Any errors encountered

Thank you for testing this!

---

**Attachments:**
- PR Link: https://github.com/seemakorani-cyber/auth0sso/pull/1 (Draft)
- Setup Script: `scripts/download_teams_transcript.py`
- Batch File: `scripts/download_transcript.bat`

