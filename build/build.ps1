# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
param(
  [string[]] $pkgDirs
)

if ($null -eq $pkgDirs) {
  $parentPath = Split-Path -parent $PSScriptRoot
  $pkgDirs = Get-ChildItem -Path $parentPath -Recurse -Filter "environment.yml" | Select-Object -ExpandProperty Directory | Split-Path -Leaf
  Write-Host "##[info]No pkgDir. Setting to default '$pkgDirs'"
}

function CreateEnv() {
  param(
    [string] $pkgDir
  )
  # Create conda environment
  $parentPath = Split-Path -parent $PSScriptRoot
  $envPath = Join-Path $parentPath $pkgDir environment.yml

  Write-Host "##[info]Build '$envPath' Conda environment"
  conda env create --quiet --file $envPath
}

foreach ($pkgDir in $pkgDirs) {
  CreateEnv -pkgDir $pkgDir
}
