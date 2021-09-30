# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Install: Install Python packages in Conda environments
        Optionally install from source or from PyPI
#>


param (
  [string] $PackageName,
  [string] $CondaEnvironmentSuffix,
  [bool] $FromSource
)

Write-Host "##[info]FromSource: '$FromSource'".

& (Join-Path $PSScriptRoot "set-env.ps1");

Import-Module (Join-Path $PSScriptRoot "conda-utils.psm1");

if ('' -eq $PackageName) {
  # If no package dir is specified, find all packages that contain an environment.yml file
  $parentPath = Split-Path -parent $PSScriptRoot
  $PackageNames = Get-ChildItem -Path $parentPath -Recurse -Filter "environment.yml" | Select-Object -ExpandProperty Directory | Split-Path -Leaf
  Write-Host "##[info]No PackageDir. Setting to default '$PackageNames'"
} else {
  $PackageNames = @($PackageName);
}

if ($null -eq $FromSource) {
  $FromSource = $True
  Write-Host "##[info]No FromSource. Setting to default '$FromSource'"
}

function Install-Package() {
  param(
    [string] $EnvName,
    [string] $PackageName
  )
  # Activate env
  Use-CondaEnv $EnvName
  # Install package
  if ($True -eq $FromSource) {
    $ParentPath = Split-Path -parent $PSScriptRoot
    $AbsPackageName = Join-Path $ParentPath $PackageName
    Write-Host "##[info]Install package $AbsPackageName in development mode for env $EnvName"
    pip install -e $AbsPackageName
  } else {
    Write-Host "##[info]Install package $PackageName for env $EnvName"
    pip install $PackageName
  }
}

if ($Env:ENABLE_PYTHON -eq "false") {
  Write-Host "##vso[task.logissue type=warning;]Skipping installing Python packages. Env:ENABLE_PYTHON was set to 'false'."
} else {
  foreach ($PackageName in $PackageNames) {
    $EnvName = ($PackageName + $CondaEnvironmentSuffix).replace("-", "")
    Install-Package -EnvName $EnvName -PackageName $PackageName
  }
}
