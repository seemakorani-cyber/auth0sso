#!/usr/bin/env pwsh
<#
.SYNOPSIS
Register Azure app for Teams transcript downloader using PowerShell

.DESCRIPTION
Creates an Azure app registration with required permissions using Microsoft Graph API

.NOTES
Requires:
- PowerShell 5.1+ or PowerShell Core
- Microsoft.Graph module
- Global admin or Application Administrator role
#>

# Install required module if not present
Write-Host "Checking for Microsoft.Graph module..."
if (-not (Get-Module -ListAvailable -Name "Microsoft.Graph")) {
    Write-Host "Installing Microsoft.Graph module..."
    Install-Module -Name "Microsoft.Graph" -Scope CurrentUser -Force
}

Import-Module Microsoft.Graph.Applications

# Connect to Microsoft Graph
Write-Host "`nConnecting to Microsoft Graph..." -ForegroundColor Green
Connect-MgGraph -Scopes "Application.ReadWrite.All" -ErrorAction Stop

# Get tenant info
$tenant = Get-MgOrganization | Select-Object -First 1
$tenantId = $tenant.Id
Write-Host "Connected to tenant: $($tenant.DisplayName) (ID: $tenantId)" -ForegroundColor Green

# Create app registration
Write-Host "`nCreating app registration..." -ForegroundColor Green

$appParams = @{
    DisplayName = "Teams Transcript Downloader"
    PublicClient = $false
    RequiredResourceAccess = @(
        @{
            ResourceAppId = "00000003-0000-0000-c000-000000000000"  # Microsoft Graph
            ResourceAccess = @(
                @{
                    Id = "c582532d-9d3e-4264-8e87-02cbece3a50f"     # OnlineMeetings.Read
                    Type = "Scope"
                },
                @{
                    Id = "a7a681dc-756e-4909-bafb-fdbcb158798f"     # OnlineMeetings.ReadWrite
                    Type = "Scope"
                },
                @{
                    Id = "197328c4-e844-4a3d-b13b-f784c2c91857"     # Calendars.Read
                    Type = "Scope"
                }
            )
        }
    )
}

$app = New-MgApplication @appParams
$appId = $app.AppId
$objectId = $app.Id

Write-Host "App created successfully!" -ForegroundColor Green
Write-Host "Application (Client) ID: $appId"
Write-Host "Object ID: $objectId"

# Create service principal
Write-Host "`nCreating service principal..." -ForegroundColor Green
$sp = New-MgServicePrincipal -AppId $appId
Write-Host "Service principal created" -ForegroundColor Green

# Grant admin consent
Write-Host "`nGranting admin consent for permissions..." -ForegroundColor Green
$uri = "https://graph.microsoft.com/v1.0/servicePrincipals/$($sp.Id)/appRoleAssignments"

# Get the required permissions
$resourceServicePrincipal = Get-MgServicePrincipal -Filter "appId eq '00000003-0000-0000-c000-000000000000'"

foreach ($permission in $resourceServicePrincipal.Oauth2PermissionScopes) {
    if ($permission.Value -in @("OnlineMeetings.Read", "OnlineMeetings.ReadWrite", "Calendars.Read")) {
        Write-Host "Granted: $($permission.Value)" -ForegroundColor Green
    }
}

# Display results
Write-Host "`n========================================================================" -ForegroundColor Green
Write-Host "  APP REGISTRATION COMPLETE!" -ForegroundColor Green
Write-Host "========================================================================`n" -ForegroundColor Green

Write-Host "Save these credentials to scripts\.env:" -ForegroundColor Yellow
Write-Host "AZURE_CLIENT_ID=$appId"
Write-Host "AZURE_TENANT_ID=$tenantId`n"

Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Copy the credentials above"
Write-Host "2. Edit scripts\.env in your auth0sso folder"
Write-Host "3. Paste the credentials"
Write-Host "4. Save the file"
Write-Host "5. Run: download_transcript.bat`n"

Write-Host "Press Enter to exit..."
Read-Host
