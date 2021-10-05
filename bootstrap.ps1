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
& (Join-Path $PSScriptRoot "build" "set-env.ps1");

# Import Conda utils
Import-Module (Join-Path $PSScriptRoot "build" "package-utils.psm1");

# Enable conda hook
Enable-Conda

# Create environment
New-CondaEnvironment -PackageName $PackageName -CondaEnvironmentSuffix $CondaEnvironmentSuffix

# Install package in environment
Install-PackageInEnv -PackageName $PackageName -CondaEnvironmentSuffix $CondaEnvironmentSuffix -FromSource $FromSource
