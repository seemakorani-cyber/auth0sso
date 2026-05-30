@echo off
setlocal enabledelayedexpansion

title Teams Transcript Downloader - Azure Setup

cls
echo.
echo ========================================================================
echo     Teams Transcript Downloader - Azure App Registration
echo ========================================================================
echo.
echo This script will create an Azure app using PowerShell.
echo.
echo Requirements:
echo   - PowerShell 5.1 or later
echo   - Global Admin or Application Administrator role
echo.

REM Check if PowerShell is available
powershell -Command "Write-Host 'PowerShell OK'" >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PowerShell is not available
    echo.
    pause
    exit /b 1
)

echo [OK] PowerShell found
echo.
echo [INFO] Starting Azure app registration...
echo.

REM Run the PowerShell script
cd /d "%~dp0"
powershell -ExecutionPolicy Bypass -File "setup_teams_auth_powershell.ps1"

if errorlevel 1 (
    echo.
    echo [ERROR] PowerShell script failed
    echo.
    pause
    exit /b 1
)

echo.
pause
