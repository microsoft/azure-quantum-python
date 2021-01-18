# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
param ($pkgDir)

if ($pkgDir -eq $null) {
  Write-Host "##[info]No pkgDir. Setting to default 'qdk'"
  $pkgDir = "qdk"
}


# Create conda environment
$parentPath = Split-Path -parent $PSScriptRoot
$envPath = Join-Path $parentPath $pkgDir environment.yml

Write-Host "##[info]Build '$envPath' Conda environment"
conda env create --quiet --file $envPath
