# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Test: Run unit tests for given packages/environments
#>

param (
  [bool] $SkipInstall
)

$PackageDir = Split-Path -parent $PSScriptRoot;
$RootDir = Split-Path -parent $PackageDir;
Import-Module (Join-Path $RootDir "build" "conda-utils.psm1");

if ($True -eq $SkipInstall) {
    Write-Host "##[info]Skipping install."
} else {
    & (Join-Path $PSScriptRoot Install-Artifacts.ps1)
}

Copy-Item -Path (Join-Path $PackageDir "tests" "unit" "*.py") -Destination $PSScriptRoot;
python -m pytest --junitxml=junit/test-results.xml
