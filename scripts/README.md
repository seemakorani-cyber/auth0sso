# Scripts

Helper scripts for the delivery-assessment workflow.

## Teams Transcript Downloader

Automatically download Teams meeting transcripts for the delivery-assessment skill.

**Quick start:**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup (one-time)
python setup_teams_auth.py

# 3. Download a transcript
python download_teams_transcript.py --meeting-name "Your Meeting Name"
```

**Full documentation:** See [`../TEAMS_TRANSCRIPT_SETUP.md`](../TEAMS_TRANSCRIPT_SETUP.md)

### Files

- **`download_teams_transcript.py`** — Main script to download transcripts
- **`setup_teams_auth.py`** — Interactive setup for Azure credentials (run once)
- **`requirements.txt`** — Python dependencies
- **`.env.example`** — Template for credentials (copy to `.env` and fill in)
- **`.env`** — Your credentials (create after running `setup_teams_auth.py`)

### Requirements

- Python 3.7+
- Azure account with Teams
- 5 minutes for one-time Azure setup

### Workflow

1. **Setup:** Run `setup_teams_auth.py` once
2. **Download:** Run `download_teams_transcript.py --meeting-name "Meeting Name"`
3. **Assess:** Open Claude Code and say "delivery assessment"

The script saves transcripts to `PM-Automations/Recordings/` where the delivery-assessment skill auto-discovers them.

