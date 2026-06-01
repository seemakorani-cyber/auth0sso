@echo off
setlocal enabledelayedexpansion

title Teams Transcript Downloader

cd /d "%~dp0"

cls
echo.
echo ========================================================================
echo          Teams Meeting Transcript Downloader
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    echo.
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo [ERROR] Credentials not configured
    echo.
    echo Please run: setup_teams.bat
    echo.
    pause
    exit /b 1
)

echo Please enter the Teams meeting name you want to download:
echo.
echo Examples:
echo   - "Project XYZ Standup"
echo   - "standup"
echo   - "weekly sync"
echo.
set /p meeting_name="Meeting name: "

if "%meeting_name%"=="" (
    echo [ERROR] Meeting name required
    echo.
    pause
    exit /b 1
)

cls
echo.
echo Downloading transcript for: "%meeting_name%"
echo.
echo [INFO] Authenticating to Teams...
echo.

python download_teams_transcript.py --meeting-name "%meeting_name%"

if errorlevel 1 (
    echo.
    echo [ERROR] Download failed
    echo.
    pause
    exit /b 1
)

echo.
echo [OK] Success!
echo.
echo Next: Open Claude Code Desktop and say "delivery assessment"
echo.
pause
