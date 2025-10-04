# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

[CmdletBinding()]
Param (
    [string] $TestFilter = ""
)

$FileFilter = "*${TestFilter}*.yaml"

# Delete old recordings
$Recordings_Folder =  Join-Path $PSScriptRoot "../tests/unit/recordings/"
if (Test-Path $Recordings_Folder) {
    Get-ChildItem $Recordings_Folder -Recurse  -Filter $FileFilter | Remove-Item -Force | Write-Verbose
}

try
{
    Push-Location (Join-Path $PSScriptRoot "../tests/")

    # Activate virtual environment if it exists
    $VenvPath = "../venv"
    if (Test-Path $VenvPath) {
        Write-Host "Activating virtual environment..."
        & "$VenvPath\Scripts\Activate.ps1"
    } else {
        Write-Warning "Virtual environment not found at $VenvPath. Please run Setup-Dev-Env.ps1 first."
    }

    if ([string]::IsNullOrEmpty($TestFilter)) {
        pytest
    }
    else {
        pytest -k $TestFilter
    }
}
finally
{
    Pop-Location
}
