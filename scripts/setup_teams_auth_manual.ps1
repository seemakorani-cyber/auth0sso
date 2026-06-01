#!/usr/bin/env pwsh
<#
.SYNOPSIS
Register Azure app using manual steps and REST API

.DESCRIPTION
Creates an Azure app registration through interactive prompts.
No module installation required - works with basic PowerShell.
#>

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Green
Write-Host "  Teams Transcript Downloader - Azure App Registration" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Since App registrations are disabled in the portal, we'll do this manually." -ForegroundColor Yellow
Write-Host ""

Write-Host "OPTION A: Use Azure CLI (Fastest)" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host ""
Write-Host "If you have Azure CLI installed (az command), run these commands:"
Write-Host ""
Write-Host "1. Login to Azure:"
Write-Host "   az login"
Write-Host ""
Write-Host "2. Create the app:"
Write-Host '   az ad app create --display-name "Teams Transcript Downloader" --public-client-redirect-uris "http://localhost"'
Write-Host ""
Write-Host "3. Copy the 'appId' from the output"
Write-Host ""
Write-Host "4. Get your tenant ID:"
Write-Host "   az account show --query tenantId"
Write-Host ""

Write-Host ""
Write-Host "OPTION B: Manual Setup (If no Azure CLI)" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host ""
Write-Host "1. Contact your Azure admin and ask them to create an app with:"
Write-Host "   - Name: 'Teams Transcript Downloader'"
Write-Host "   - Public client: Yes"
Write-Host "   - Permissions:"
Write-Host "     * Microsoft Graph: OnlineMeetings.Read"
Write-Host "     * Microsoft Graph: OnlineMeetings.ReadWrite"
Write-Host "     * Microsoft Graph: Calendars.Read"
Write-Host ""
Write-Host "2. Get these from the app:"
Write-Host "   - Application (Client) ID"
Write-Host "   - Directory (Tenant) ID"
Write-Host ""

Write-Host ""
Write-Host "OPTION C: PowerShell (Advanced)" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Write-Host ""
Write-Host "If you have Application Administrator role, run this:"
Write-Host ""
Write-Host "  Connect-AzureAD"
Write-Host '  New-AzureADApplication -DisplayName "Teams Transcript Downloader" -PublicClient $true'
Write-Host ""
Write-Host "Then go to Settings > API Permissions and add the 3 permissions listed above"
Write-Host ""

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Green
Write-Host "Once you have Client ID and Tenant ID:" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
Write-Host ""

$clientId = Read-Host "Enter Application (Client) ID"
$tenantId = Read-Host "Enter Directory (Tenant) ID"

if ([string]::IsNullOrWhiteSpace($clientId) -or [string]::IsNullOrWhiteSpace($tenantId)) {
    Write-Host ""
    Write-Host "[ERROR] Both IDs are required" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create .env file
$envPath = Split-Path -Parent $PSCommandPath
$envFile = Join-Path $envPath ".env"

$envContent = @"
# Azure credentials for Teams transcript download
AZURE_CLIENT_ID=$clientId
AZURE_TENANT_ID=$tenantId
"@

Set-Content -Path $envFile -Value $envContent
Write-Host ""
Write-Host "========================================================================" -ForegroundColor Green
Write-Host "  [OK] SETUP COMPLETE!" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Credentials saved to: $envFile" -ForegroundColor Green
Write-Host ""
Write-Host "You can now download transcripts with:" -ForegroundColor Cyan
Write-Host "  - Double-click download_transcript.bat" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"
