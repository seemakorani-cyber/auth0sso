@echo off
setlocal enabledelayedexpansion

title Teams Transcript Downloader

cd /d "%~dp0"

:menu
cls
echo.
echo ========================================================================
echo     Teams Transcript Downloader
echo ========================================================================
echo.
echo What would you like to do?
echo.
echo   [1] Download a Teams transcript
echo   [2] Setup (Python dependencies)
echo   [3] Exit
echo.
set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    call download_transcript.bat
    goto menu
) else if "%choice%"=="2" (
    call setup_teams.bat
    goto menu
) else if "%choice%"=="3" (
    exit /b 0
) else (
    echo.
    echo [ERROR] Invalid choice
    echo.
    pause
    goto menu
)
