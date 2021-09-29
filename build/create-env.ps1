# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Create Conda environment(s) for given package directories
        Optionally, use EnvSuffix to specify a special environment file with name environment<EnvSuffix>.yml.
#>

param(
  [string] $PackageDir,
  [string] $EnvSuffix
)

if ('' -eq $PackageDir) {
  # If no package dir is specified, find all packages that contain an environment.yml file
  $parentPath = Split-Path -parent $PSScriptRoot
  $PackageDirs = Get-ChildItem -Path $parentPath -Recurse -Filter "environment.yml" | Select-Object -ExpandProperty Directory | Split-Path -Leaf
  Write-Host "##[info]No PackageDir. Setting to default '$PackageDirs'"
} else {
  $PackageDirs = @($PackageDir);
}

foreach ($PackageDir in $PackageDirs) {
  $parentPath = Split-Path -parent $PSScriptRoot
  if ('' -ne $EnvSuffix) {
    $EnvPath = (Join-Path (Join-Path $parentPath $PackageDir) "environment$EnvSuffix.yml")
    $EnvName = ($PackageDir + $EnvSuffix).replace("-", "")
  } else {
    $EnvPath = (Join-Path (Join-Path $parentPath $PackageDir) "environment.yml")
    $EnvName = $PackageDir.replace("-", "")
  }

  # Check if environment already exists
  $EnvExists = conda env list | Select-String -Pattern "$EnvName " | Measure-Object | Select-Object -Exp Count

  # If it exists, skip creation
  if ($EnvExists -eq "1") {
      Write-Host "##[info]Skipping creating $EnvName; env already exists."

  } else {
      # If it does not exist, create conda environment
      Write-Host "##[info]Build '$EnvPath' Conda environment"
      conda env create --quiet --file $EnvPath
  }    
}
