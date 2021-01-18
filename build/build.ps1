# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
param ($pkgDir)

if ($pkgDir -eq $null) {
  Write-Host "##[info]No pkgDir. Setting to default 'qdk'"
  $pkgDir = "qdk"
}

Write-Host "##[info]Build '$pkgDir' Conda environment"

# Create conda environment
conda env create --quiet --file $pkgDir/environment.yml
