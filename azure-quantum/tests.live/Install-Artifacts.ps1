# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Bootstrap: set up a Python environment using Anaconda
#>

$PackageDir = Split-Path -parent $PSScriptRoot;
$RootDir = Split-Path -parent $PackageDir;
Import-Module (Join-Path $RootDir "build" "conda-utils.psm1");

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
    & (Join-Path $RootDir build create-env.ps1) -PackageDirs $PackageDir
}

# Install package from source
& (Join-Path $RootDir build build.ps1) -PackageDirs $PackageDir
