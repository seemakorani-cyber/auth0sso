@echo off
setlocal enabledelayedexpansion

title Teams Transcript Setup

cd /d "%~dp0"

echo.
echo ========================================================================
echo     Teams Transcript Downloader - Setup
echo ========================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed
    echo.
    echo Please install Python 3.7+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

echo [INFO] Configuring credentials...
REM Create .env file with credentials
(
    echo # Azure credentials for Teams transcript download
    echo AZURE_CLIENT_ID=22cd99bd-a84b-4739-95cc-18a43f48acf1
    echo AZURE_TENANT_ID=d508624f-a0b7-4fd3-9511-05b18ca02784
    echo AZURE_CLIENT_SECRET=your-client-secret-here
) > .env

echo [OK] Credentials template created in .env
echo.
echo IMPORTANT: Edit .env and replace:
echo   your-client-secret-here
echo with your actual client secret from Azure
echo.

echo [INFO] Installing Python dependencies...
pip install msal requests python-dotenv -q

echo [OK] Setup complete!
echo.
echo 1. Edit .env and add your client secret
echo 2. Double-click: download_transcript.bat
echo.
pause
