# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

<#
.SYNOPSIS
(Re)Generate the underlying Azure Quantum Python data-Plane client for the CLI based on the latest published Swagger.
.DESCRIPTION
(Re)Generate the underlying Azure Quantum Python data-Plane client for the CLI based on the latest published Swagger.
.PARAMETER SwaggerRepoUrl
The URL of the git repo that contains the Swagger and AutoRest ReadMe.md configurations (defaults to "https://github.com/Azure/azure-rest-api-specs")
.PARAMETER SwaggerRepoBranch
The name of the swagger repo branch (defaults to "main")
.PARAMETER SwaggerTagVersion
The Swagger version to be used (defaults to "", which will use the default tag from the main ReadMe.md)

.EXAMPLE
./eng/Generate-DataPlane-Client.ps1

# Regenerate the data-plane client using the latest published Swagger from the official repo

.EXAMPLE
./eng/Generate-DataPlane-Client.ps1 -SwaggerRepoBranch "feature/quantum/update-clients"

# Regenerate the data-plane client using the Swagger from the official repo, but from a feature branch

.EXAMPLE
./eng/Generate-DataPlane-Client.ps1 -SwaggerTagVersion "package-2019-11-04-preview"

# Regenerate the data-plane client using the an older version of the Swagger

#>

[CmdletBinding()]
Param (
    [string] $SwaggerRepoUrl = "https://github.com/Azure/azure-rest-api-specs",
    [string] $SwaggerRepoBranch = "main",
    [string] $SwaggerTagVersion
)

$PackageVersion = $env:PYTHON_VERSION 
if ([string]::IsNullOrEmpty($PackageVersion)) {
    $VersionFilePath = Join-Path $PSScriptRoot "../azure/quantum/version.py"
    if (Test-Path $VersionFilePath) {
        $VersionFileContent = Get-Content -Path $VersionFilePath
        $PackageVersion = [regex]::Match($VersionFileContent, '__version__\s*=\s*"(?<version>[^"]+)"').Groups["version"]?.Value
    }
}
if ([string]::IsNullOrEmpty($PackageVersion)) {
    $PackageVersion = "0.0.0.1"
}

$OutputFolder = Join-Path $PSScriptRoot "../azure/quantum/_client/"

$AutoRestConfig = "$SwaggerRepoUrl/blob/$SwaggerRepoBranch/specification/quantum/data-plane/readme.md"

Write-Verbose "Installing latest AutoRest client"
npm install -g autorest@latest | Write-Verbose

if ([string]::IsNullOrEmpty($SwaggerTagVersion))
{
    Write-Verbose "Generating the client based on:`nConfig: $AutoRestConfig"
    autorest $AutoRestConfig `
        --verbose `
        --python `
        --python-mode=cli `
        --output-folder=$OutputFolder `
        --package-version=$PackageVersion `
        | Write-Verbose
}
else
{
    Write-Verbose "Generating the client based on:`nConfig: $AutoRestConfig`nTag: $SwaggerTagVersion"
    autorest $AutoRestConfig `
        --verbose `
        --python `
        --python-mode=cli `
        --tag=$SwaggerTagVersion `
        --output-folder=$OutputFolder `
        --package-version=$PackageVersion `
        | Write-Verbose
}
