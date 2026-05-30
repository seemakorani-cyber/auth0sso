@echo off
setlocal enabledelayedexpansion

REM Teams Transcript Setup - One-time configuration

title Teams Transcript Downloader - Setup

cls
echo.
echo ========================================================================
echo     Teams Transcript Downloader - SETUP
echo     One-time configuration (takes ~5 minutes)
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python 3.7+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Get the script directory
cd /d "%~dp0"

REM Check if requirements are installed
echo [INFO] Checking Python dependencies...
python -c "import msal" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies (msal, requests, python-dotenv)...
    echo.
    pip install msal requests python-dotenv
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
    echo.
) else (
    echo [OK] Dependencies already installed
    echo.
)

REM Run the setup script
echo [INFO] Starting Azure app registration setup...
echo.
python setup_teams_auth.py

if errorlevel 1 (
    echo.
    echo [ERROR] Setup failed. Please try again.
    pause
    exit /b 1
)

echo.
echo ========================================================================
echo  [OK] SETUP COMPLETE!
echo ========================================================================
echo.
echo You can now download transcripts by running:
echo   - Double-click "download_transcript.bat"
echo.
echo Or from command line:
echo   python download_teams_transcript.py --meeting-name "Meeting Name"
echo.
pause
