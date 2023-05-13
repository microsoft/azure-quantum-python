# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Test: Run unit tests for given packages/environments.
        If no PackageName is specified, this script searches the root directory and runs
        the tests for all packages.
#>

param (
  [string] $PackageName,
  [string] $CondaEnvironmentSuffix
)

& (Join-Path $PSScriptRoot "set-env.ps1");

Import-Module (Join-Path $PSScriptRoot "package-utils.psm1");



# Pin urllib3 for compatibility with vcrpy
Write-Host "##[info]Install version of urllib3 that is compatible with vcrpy"
pip install urllib3==1.26.15

if ($Env:ENABLE_PYTHON -eq "false") {
  Write-Host "##vso[task.logissue type=warning;]Skipping testing Python packages. Env:ENABLE_PYTHON was set to 'false'."
} else {
  $PackageNames = PackagesList -PackageName $PackageName
  $ExitCode = 0;
  foreach ($PackageName in $PackageNames) {
    $EnvName = GetEnvName -PackageName $PackageName -CondaEnvironmentSuffix $CondaEnvironmentSuffix
    "Testing package $PackageName in environment $EnvName" | Write-Host
    $Success = Invoke-Tests -PackageName $PackageName -EnvName $EnvName
    "Result of Invoke-Tests: $Success" | Write-Host
    if ($Success -ne $True) {
        $ExitCode = 1;
        Write-Host "##vso[task.logissue type=error;]Tests for package $PackageName failed."
      }
    }

    "Returning: $ExitCode" | Write-Host
    exit $ExitCode;
}
