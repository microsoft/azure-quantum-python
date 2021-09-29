# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Create Conda environment(s) for given package directories
        Optionally, use CondaEnvironmentSuffix to specify a special environment file with name environment<CondaEnvironmentSuffix>.yml.
#>

param(
  [string] $PackageName,
  [string] $CondaEnvironmentSuffix
)

if ('' -eq $PackageName) {
  # If no package dir is specified, find all packages that contain an environment.yml file
  $parentPath = Split-Path -parent $PSScriptRoot
  $PackageNames = Get-ChildItem -Path $parentPath -Recurse -Filter "environment.yml" | Select-Object -ExpandProperty Directory | Split-Path -Leaf
  Write-Host "##[info]No PackageDir. Setting to default '$PackageNames'"
} else {
  $PackageNames = @($PackageName);
}

foreach ($PackageName in $PackageNames) {
  $parentPath = Split-Path -parent $PSScriptRoot
  if ('' -ne $CondaEnvironmentSuffix) {
    $EnvPath = (Join-Path (Join-Path $parentPath $PackageName) "environment$CondaEnvironmentSuffix.yml")
    $EnvName = ($PackageName + $CondaEnvironmentSuffix).replace("-", "")
  } else {
    $EnvPath = (Join-Path (Join-Path $parentPath $PackageName) "environment.yml")
    $EnvName = $PackageName.replace("-", "")
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
