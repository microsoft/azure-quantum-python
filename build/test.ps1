# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
param ($envName, $pkgDir)
if ($envName -eq $null) {
  Write-Host "##[info]No envName. Setting to default 'qdk'."
  $envName = "qdk"
}

if ($pkgDir -eq $null) {
  Write-Host "##[info]No pkgDir. Setting to envName '$envName'"
  $pkgDir = $envName
}

$parentPath = Split-Path -parent $PSScriptRoot
$AbsPkgDir = Join-Path $parentPath $pkgDir

Write-Host "##[info]Install package $AbsPkgDir in development mode and run tests for env $envName"
sh $PSScriptRoot/test.sh $envName $AbsPkgDir
