# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Test: Run unit tests for given packages/environments
#>

param (
  [string[]] $PackageDirs,
  [string[]] $EnvNames
)

& (Join-Path $PSScriptRoot "set-env.ps1");

Import-Module (Join-Path $PSScriptRoot "conda-utils.psm1");

if ($null -eq $PackageDirs) {
  $ParentPath = Split-Path -parent $PSScriptRoot
  $PackageDirs = Get-ChildItem -Path $ParentPath -Recurse -Filter "environment.yml" | Select-Object -ExpandProperty Directory | Split-Path -Leaf
  Write-Host "##[info]No PackageDir. Setting to default '$PackageDirs'"
}

if ($null -eq $EnvNames) {
  $EnvNames = $PackageDirs | ForEach-Object {$_.replace("-", "")}
  Write-Host "##[info]No EnvNames. Setting to default '$EnvNames'"
}

# Check that input is valid
if ($EnvNames.length -ne $PackageDirs.length) {
  throw "Cannot run build script: '$EnvNames' and '$PackageDirs' lengths don't match"
}

function Invoke-Tests() {
  param(
    [string] $PackageDir,
    [string] $EnvName
  )
  $PkgName = $PackageDir.replace("-", ".")
  $ParentPath = Split-Path -parent $PSScriptRoot
  $AbsPackageDir = Join-Path $ParentPath $PackageDir
  Write-Host "##[info]Test package $AbsPackageDir and run tests for env $EnvName"
  # Activate env
  Use-CondaEnv $EnvName
  # Install testing deps
  python -m pip install --upgrade pip
  pip install pytest pytest-azurepipelines pytest-cov pylint
  # Run pylint
  pylint -f msvs $AbsPackageDir
  # Run tests
  pytest --cov-report term --cov=$PkgName $AbsPackageDir
}

if ($Env:ENABLE_PYTHON -eq "false") {
  Write-Host "##vso[task.logissue type=warning;]Skipping testing Python packages. Env:ENABLE_PYTHON was set to 'false'."
} else {
  for ($i=0; $i -le $PackageDirs.length-1; $i++) {
    Invoke-Tests -PackageDir $PackageDirs[$i] -EnvName $EnvNames[$i]
  }
}
