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
Write-Host $FromSource;

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

if ($PackageName -eq "azure-quantum") {
  # Since we may be using the Q# container image instead 
  # of a regular build agent image, we may need to install the .NET SDK
  $installDotnet = !(Get-Command dotnet -ErrorAction SilentlyContinue)
  if ($installDotnet) {
    apt-get update
    apt-get install -y dotnet-sdk-6.0
    $env:DOTNET_ROOT = "$env:HOME/.dotnet"
    $env:PATH += ";$env:DOTNET_ROOT;$env:DOTNET_ROOT/tools"
  }

  # Installs IQ# dotnet tool, IQ# kernel and the qsharp Python package
  # Used for running tests between the Azure Quantum Python SDK and IQ# (Q#+QIR job submission)
  & (Join-Path $PSScriptRoot "build" "install-iqsharp.ps1");
}