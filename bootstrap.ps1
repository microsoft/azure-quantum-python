# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Bootstrap: set up a Python environment using Anaconda using the corresponding
        environment.yml file. Install the specified package in the environment,
        either from Source or from PyPI. Takes optional input arguments PackageName,
        CondaEnvironmentSuffix and FromSource:
        
          If no PackageName is specified, this script searches the root directory and runs
        bootstrap for all packages.
          
          The CondaEnvironmentSuffix is used to find an alternate environment yml, for
        instance environment<CondaEnvironmentSuffix>.yml.
          
          FromSource determines if the package is installed from source using
        <pip install -e> and defaults to True.
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
