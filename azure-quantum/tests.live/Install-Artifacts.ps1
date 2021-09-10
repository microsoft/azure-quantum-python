# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Bootstrap: set up a Python environment using Anaconda
#>

$packageDir = Split-Path -parent $PSScriptRoot;
$rootDir = Split-Path -parent $packageDir;
Import-Module (Join-Path $rootDir "build" "conda-utils.psm1");

# Enable conda hook
Enable-Conda

# Check if environment already exists
$EnvName = $PackageDir.replace("-", "")
$EnvExists = conda env list | Select-String -Pattern "$EnvName " | Measure-Object | Select-Object -Exp Count
# if it exists, skip creation
if ($EnvExists -eq "1") {
    Write-Host "##[info]Skipping creating $EnvName; env already exists."
} else {
    # if it doese not exist, create env
    & (Join-Path $rootDir build create-env.ps1) -PackageDirs $PackageDir
}

# Install package from source
& (Join-Path $rootDir build build.ps1) -PackageDirs $PackageDir
