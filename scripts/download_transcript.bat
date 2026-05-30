@echo off
setlocal enabledelayedexpansion

title Teams Transcript Downloader

cls
echo.
echo ========================================================================
echo          Teams Meeting Transcript Downloader
echo ========================================================================
echo.

REM Check if setup has been done
if not exist ".env" (
    echo [WARNING] Setup not complete!
    echo.
    echo You need to run "setup_teams.bat" first to configure credentials.
    echo.
    set /p setup_choice="Enter Y to setup or N to exit (Y/N): "

    if "%setup_choice%"=="Y" (
        call setup_teams.bat
        if errorlevel 1 (
            exit /b 1
        )
    ) else (
        echo.
        echo [ERROR] Setup required to continue. Exiting.
        pause
        exit /b 1
    )
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not found or not in PATH
    echo.
    echo Please install Python 3.7+ from https://www.python.org/
    echo.
    pause
    exit /b 1
)

REM Get current directory
cd /d "%~dp0"

echo.
echo Please enter the Teams meeting name (or partial name)
echo.
echo Examples:
echo   - "Project XYZ Standup"
echo   - "standup"
echo   - "weekly sync"
echo.
set /p meeting_name="Meeting name: "

if "%meeting_name%"=="" (
    echo.
    echo [ERROR] Meeting name cannot be empty
    echo.
    pause
    exit /b 1
)

cls
echo.
echo ========================================================================
echo          Downloading Transcript
echo ========================================================================
echo.
echo Meeting name: "%meeting_name%"
echo.
echo [INFO] Authenticating to Teams...
echo.

REM Run the Python script
python download_teams_transcript.py --meeting-name "%meeting_name%"

if errorlevel 1 (
    echo.
    echo ========================================================================
    echo  [ERROR] DOWNLOAD FAILED
    echo ========================================================================
    echo.
    echo Possible issues:
    echo   - Meeting name not found - try a shorter or different name
    echo   - Transcript not ready - Teams takes 5-10 min after meeting ends
    echo   - Credentials expired - re-run setup_teams.bat
    echo.
    echo For more help, see: TEAMS_TRANSCRIPT_SETUP.md
    echo.
    pause
    exit /b 1
)

REM Success
cls
echo.
echo ========================================================================
echo  [OK] TRANSCRIPT DOWNLOADED SUCCESSFULLY!
echo ========================================================================
echo.
echo Next step:
echo   1. Open Claude Code Desktop
echo   2. Say: "delivery assessment" or "assess my team"
echo   3. The skill will auto-discover the transcript
echo   4. Review the generated Confluence report
echo.
pause
