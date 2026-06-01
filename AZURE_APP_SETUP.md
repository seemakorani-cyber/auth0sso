# Azure App Registration Setup

## Required Configuration for Teams Transcript Downloader

The Teams Transcript Downloader uses device flow authentication, which requires the Azure app to be configured correctly.

### Steps to Configure

1. **Go to Azure Portal** → App registrations → Find the Teams Transcript app
   
2. **Click on Authentication** (left menu)

3. **Add a platform:**
   - Click "+ Add a platform"
   - Select "Mobile and desktop applications"
   
4. **Add redirect URI:**
   - Add: `http://localhost`
   - Click "Configure"
   - Save

5. **Verify Configuration:**
   - Platform should show: "Mobile and desktop applications"
   - Redirect URIs should include: `http://localhost`

### What This Enables

✅ Device flow (browser-based login)  
✅ Multi-Factor Authentication (MFA) support  
✅ No passwords stored  
✅ Secure token caching  

### Device Flow Login Experience

When users run the downloader:

1. Terminal displays a login code and URL
2. User opens the URL in their browser
3. User enters the code
4. Completes Teams login (with MFA if enabled)
5. Script receives token automatically
6. Transcript downloads

### App Registration Details

- **Client ID:** `22cd99bd-a84b-4739-95cc-18a43f48acf1`
- **Tenant ID:** `d508624f-a0b7-4fd3-9511-05b18ca02784`
- **API Permissions:** Calendars.Read, OnlineMeetings.Read

---

Once configured, users can run: `download_transcript.bat` or `python download_teams_transcript.py --meeting-name "standup"`
