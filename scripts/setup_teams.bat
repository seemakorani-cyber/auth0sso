@echo off
setlocal enabledelayedexpansion

title Teams Transcript Downloader - Setup

cls
echo.
echo ========================================================================
echo     Teams Transcript Downloader - Setup
echo ========================================================================
echo.
echo Since App registrations are disabled in your Azure portal,
echo you have these options:
echo.
echo [1] I have Azure CLI installed (fastest)
echo [2] I'll ask my Azure admin (easiest)
echo [3] I have Application Administrator role (advanced)
echo [4] Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    cls
    echo.
    echo ========================================================================
    echo   Option 1: Using Azure CLI
    echo ========================================================================
    echo.
    echo Run these commands in PowerShell or Command Prompt:
    echo.
    echo 1. Login to Azure:
    echo    az login
    echo.
    echo 2. Create the app:
    echo    az ad app create --display-name "Teams Transcript Downloader" --public-client-redirect-uris "http://localhost"
    echo.
    echo 3. Copy the "appId" from the output (looks like: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)
    echo.
    echo 4. Get your tenant ID:
    echo    az account show --query tenantId
    echo.
    echo 5. Copy the output (another ID like appId)
    echo.
    set /p client_id="Paste the appId here: "
    set /p tenant_id="Paste the tenantId here: "

    goto save_credentials

) else if "%choice%"=="2" (
    cls
    echo.
    echo ========================================================================
    echo   Option 2: Ask Your Azure Admin
    echo ========================================================================
    echo.
    echo Send this to your Azure admin:
    echo.
    echo "Please create an Azure app with these settings:"
    echo "  - App name: Teams Transcript Downloader"
    echo "  - Account type: Multitenant"
    echo "  - Redirect URI: Public client/native"
    echo.
    echo "Then add these API permissions (Microsoft Graph):"
    echo "  - OnlineMeetings.Read (delegated)"
    echo "  - OnlineMeetings.ReadWrite (delegated)"
    echo "  - Calendars.Read (delegated)"
    echo.
    echo "Grant admin consent"
    echo.
    echo "Send me the:"
    echo "  - Application (Client) ID"
    echo "  - Directory (Tenant) ID"
    echo.
    set /p client_id="Paste the Application (Client) ID: "
    set /p tenant_id="Paste the Directory (Tenant) ID: "

    goto save_credentials

) else if "%choice%"=="3" (
    cls
    echo.
    echo ========================================================================
    echo   Option 3: Using PowerShell (Advanced)
    echo ========================================================================
    echo.
    echo Run these commands in PowerShell:
    echo.
    echo 1. Connect to Azure:
    echo    Connect-AzureAD
    echo.
    echo 2. Create app:
    echo    $app = New-AzureADApplication -DisplayName "Teams Transcript Downloader" -PublicClient $true
    echo    $app.AppId
    echo    $app.ObjectId
    echo.
    echo 3. Get tenant ID:
    echo    (Get-AzureADTenantDetail).ObjectId
    echo.
    echo 4. Add API permissions manually in Azure portal or use:
    echo    $sp = Get-AzureADServicePrincipal -Filter "appId eq '00000003-0000-0000-c000-000000000000'"
    echo    Then grant the 3 permissions
    echo.
    set /p client_id="Paste the Application (Client) ID: "
    set /p tenant_id="Paste the Tenant ID: "

    goto save_credentials

) else if "%choice%"=="4" (
    exit /b 0
) else (
    echo.
    echo [ERROR] Invalid choice
    echo.
    pause
    goto %0
)

:save_credentials
if "%client_id%"=="" (
    echo.
    echo [ERROR] Client ID cannot be empty
    echo.
    pause
    exit /b 1
)

if "%tenant_id%"=="" (
    echo.
    echo [ERROR] Tenant ID cannot be empty
    echo.
    pause
    exit /b 1
)

REM Create .env file
cd /d "%~dp0"
(
    echo # Azure credentials for Teams transcript download
    echo AZURE_CLIENT_ID=%client_id%
    echo AZURE_TENANT_ID=%tenant_id%
) > .env

cls
echo.
echo ========================================================================
echo  [OK] SETUP COMPLETE!
echo ========================================================================
echo.
echo Credentials saved to: .env
echo.
echo Client ID: %client_id%
echo Tenant ID: %tenant_id%
echo.
echo Next steps:
echo   1. Double-click: download_transcript.bat
echo   2. Enter your Teams meeting name
echo   3. Transcript downloads automatically
echo.
pause
