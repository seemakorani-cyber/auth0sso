@echo off
setlocal enabledelayedexpansion

title Teams Transcript Downloader - Azure Setup

cls
echo.
echo ========================================================================
echo     Teams Transcript Downloader - Azure App Registration
echo ========================================================================
echo.
echo Since App registrations are disabled in your portal, we'll use
echo alternative methods to create the app.
echo.

cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "setup_teams_auth_manual.ps1"

if errorlevel 1 (
    echo.
    echo [ERROR] Setup failed
    echo.
    pause
    exit /b 1
)

echo.
pause
