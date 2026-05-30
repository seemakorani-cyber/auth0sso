@echo off
setlocal enabledelayedexpansion

title Teams Transcript Downloader - Main Menu

:menu
cls
echo.
echo ========================================================================
echo         Teams Transcript Downloader - Main Menu
echo ========================================================================
echo.
echo What would you like to do?
echo.
echo   [1] Download a Teams transcript
echo   [2] Setup (first-time only)
echo   [3] Open documentation
echo   [4] Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    call download_transcript.bat
    goto menu
) else if "%choice%"=="2" (
    call setup_teams.bat
    goto menu
) else if "%choice%"=="3" (
    if exist "..\TEAMS_TRANSCRIPT_SETUP.md" (
        start notepad "..\TEAMS_TRANSCRIPT_SETUP.md"
    ) else (
        echo.
        echo [ERROR] Documentation file not found
        echo.
        pause
    )
    goto menu
) else if "%choice%"=="4" (
    exit /b 0
) else (
    echo.
    echo [ERROR] Invalid choice. Please enter 1, 2, 3, or 4.
    echo.
    pause
    goto menu
)
