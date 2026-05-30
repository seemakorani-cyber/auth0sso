@echo off
setlocal enabledelayedexpansion

title Teams Transcript Downloader - Setup

cls
echo.
echo ========================================================================
echo     Teams Transcript Downloader - SETUP
echo     One-time configuration
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

REM Install dependencies
echo [INFO] Installing Python dependencies...
echo.
pip install msal requests python-dotenv

if errorlevel 1 (
    echo.
    echo [WARNING] Failed to install Python dependencies
    echo.
    echo This might be due to:
    echo   - Network issues
    echo   - Python not in PATH
    echo.
    set /p choice="Try PowerShell-based Azure setup instead? (Y/N): "
    if "%choice%"=="Y" (
        call setup_teams_auth_azure.bat
    ) else (
        echo [ERROR] Cannot continue without dependencies
        pause
        exit /b 1
    )
    exit /b 0
)

echo.
echo [OK] Dependencies installed
echo.

REM Run the setup script
echo [INFO] Starting Azure app registration setup...
echo.
python setup_teams_auth.py

if errorlevel 1 (
    echo.
    echo [INFO] Python setup failed. Trying PowerShell setup...
    echo.
    call setup_teams_auth_azure.bat
    exit /b 0
)

echo.
echo ========================================================================
echo  [OK] SETUP COMPLETE!
echo ========================================================================
echo.
echo You can now download transcripts by running:
echo   - Double-click "download_transcript.bat"
echo.
pause
