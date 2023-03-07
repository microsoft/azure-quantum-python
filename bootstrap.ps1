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
          
          FromWheel determines if the package is installed from a wheel on PyPI (if True)
          or from source using <pip install -e> (if False) and defaults to False.
#>

param(
  [string] $PackageName,
  [string] $CondaEnvironmentSuffix,
  [bool] $FromWheel
)

if ($False -eq $FromWheel) {
  $FromSource = $True;
} else {
  $FromSource = $False;
}
Write-Host "From source: $FromSource";

# Set env vars
& (Join-Path $PSScriptRoot "build/set-env.ps1");

Write-Host "PATH: $env:PATH";
Write-Host "Path: $env:Path";
#Write-Host "dotnet: $(&(which dotnet))";
Write-Host "Agent.ToolsDirectory: $(Agent.ToolsDirectory)";
Write-Host "Agent.ToolsDirectory: $(Test-Path "$(Agent.ToolsDirectory)/dotnet")";

# Import Conda utils
Import-Module (Join-Path $PSScriptRoot "build/package-utils.psm1");

# Enable conda hook
Enable-Conda

# Create environment
New-CondaEnvironment -PackageName $PackageName -CondaEnvironmentSuffix $CondaEnvironmentSuffix *>&1

# Install package in environment
Install-PackageInEnv -PackageName $PackageName -CondaEnvironmentSuffix $CondaEnvironmentSuffix -FromSource $FromSource *>&1

# Installs IQ# dotnet tool, IQ# kernel and the qsharp Python package
# Used for running tests between the Azure Quantum Python SDK and IQ# (Q#+QIR job submission)
& (Join-Path $PSScriptRoot "build/install-iqsharp.ps1");
