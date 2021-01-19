# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
param (
  [string[]] $envNames,
  [string[]] $pkgDirs
)

if ($null -eq $pkgDirs) {
  $parentPath = Split-Path -parent $PSScriptRoot
  $pkgDirs = Get-ChildItem -Path $parentPath -Recurse -Filter "environment.yml" | Select-Object -ExpandProperty Directory | Split-Path -Leaf
  Write-Host "##[info]No pkgDir. Setting to default '$pkgDirs'"
}

if ($null -eq $envNames) {
  $envNames = $pkgDirs | ForEach-Object {$_.replace("-","")}
  Write-Host "##[info]No envNames. Setting to default '$envNames'"
}


function RunTests() {
  param(
    [string] $envName,
    [string] $pkgDir
  )
  $parentPath = Split-Path -parent $PSScriptRoot
  $AbsPkgDir = Join-Path $parentPath $pkgDir
  Write-Host "##[info]Install package $AbsPkgDir in development mode and run tests for env $envName"
  # Set environment vars to be able to run conda activate
  (& conda "shell.powershell" "hook") | Out-String | Invoke-Expression
  # Activate env
  conda activate $envName
  which python
  # Install testing deps
  python -m pip install --upgrade pip
  pip install pytest pytest-azurepipelines
  # Install package
  pip install -e $AbsPkgDir
  # Run tests
  pytest $AbsPkgDir
}

for ($i=0; $i -le $pkgDirs.length-1; $i++) {
  RunTests -envName $envNames[$i] -pkgDir $pkgDirs[$i]
}
