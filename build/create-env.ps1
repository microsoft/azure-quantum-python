# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

##
# Create Conda environment(s) for given package directories
##
param(
  [string[]] $PackageDirs
)

if ($null -eq $PackageDirs) {
  $parentPath = Split-Path -parent $PSScriptRoot
  $PackageDirs = Get-ChildItem -Path $parentPath -Recurse -Filter "environment.yml" | Select-Object -ExpandProperty Directory | Split-Path -Leaf
  Write-Host "##[info]No PackageDir. Setting to default '$PackageDirs'"
}

function New-Environment() {
  param(
    [string] $PackageDir
  )
  # Create conda environment
  $parentPath = Split-Path -parent $PSScriptRoot
  $EnvPath = Join-Path $parentPath $PackageDir environment.yml

  Write-Host "##[info]Build '$EnvPath' Conda environment"
  conda env create --quiet --file $EnvPath
}

foreach ($PackageDir in $PackageDirs) {
  New-Environment -PackageDir $PackageDir
}
