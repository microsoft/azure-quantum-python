# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Bootstrap: set up a Python environment using Anaconda
#>

param(
  [string] $PackageName,
  [string] $CondaEnvironmentSuffix,
  [bool] $FromSource
)

# Set env vars
& (Join-Path (Join-Path $PSScriptRoot "build") "set-env.ps1");

# Import Conda utils
Import-Module (Join-Path (Join-Path $PSScriptRoot "build") "conda-utils.psm1");

# Enable conda hook
Enable-Conda

# Create environment
& (Join-Path (Join-Path $PSScriptRoot build) create-env.ps1) -PackageName $PackageName -CondaEnvironmentSuffix $CondaEnvironmentSuffix

# Install package in environment
& (Join-Path (Join-Path $PSScriptRoot build) install.ps1) -PackageNames $PackageName -EnvNames $PackageName$CondaEnvironmentSuffix -FromSource $FromSource
