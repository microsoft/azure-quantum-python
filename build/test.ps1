# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Test: Run unit tests for given packages/environments
#>

param (
  [string] $PackageName,
  [string] $CondaEnvironmentSuffix
)

& (Join-Path $PSScriptRoot "set-env.ps1");

Import-Module (Join-Path $PSScriptRoot "conda-utils.psm1");

if ('' -eq $PackageName) {
  # If no package name is specified, find all packages that contain an environment.yml file
  $parentPath = Split-Path -parent $PSScriptRoot
  $PackageNames = Get-ChildItem -Path $parentPath -Recurse -Filter "environment.yml" | Select-Object -ExpandProperty Directory | Split-Path -Leaf
  Write-Host "##[info]No PackageDir. Setting to default '$PackageNames'"
} else {
  $PackageNames = @($PackageName);
}

function Invoke-Tests() {
  param(
    [string] $PackageName,
    [string] $EnvName
  )
  $PkgName = $PackageName.replace("-", ".")
  $ParentPath = Split-Path -parent $PSScriptRoot
  $AbsPackageDir = Join-Path $ParentPath $PackageName
  $EnvName = $EnvName.replace("-", "")
  Write-Host "##[info]Test package $AbsPackageDir and run tests for env $EnvName"
  # Activate env
  Use-CondaEnv $EnvName
  # Install testing deps
  python -m pip install --upgrade pip
  pip install pytest pytest-azurepipelines pytest-cov
  # Run tests
  pytest --cov-report term --cov=$PkgName $AbsPackageDir
}

if ($Env:ENABLE_PYTHON -eq "false") {
  Write-Host "##vso[task.logissue type=warning;]Skipping testing Python packages. Env:ENABLE_PYTHON was set to 'false'."
} else {
  foreach ($PackageName in $PackageNames) {
    $EnvName = ($PackageName + $CondaEnvironmentSuffix).replace("-", "")
    Invoke-Tests -PackageName $PackageName -EnvName $EnvName
  }
}
