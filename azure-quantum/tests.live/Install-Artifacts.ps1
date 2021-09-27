# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Install-Artifacts: set up a Python environment using Anaconda
#>

$PackageDir = Split-Path -parent $PSScriptRoot;
$RootDir = Split-Path -parent $PackageDir;
Import-Module (Join-Path $RootDir "build" "conda-utils.psm1");

<# 
    Install From Source
#>
function Install-FromSource() {
    & (Join-Path $RootDir build build.ps1) -PackageDirs $PackageDir
}

<# 
    Install From Build Artifacts
#>
function Install-FromBuild() {
    Push-Location $Env:PYTHON_OUTDIR
        "Installing $PackageDir wheels from $Env:PYTHON_OUTDIR" | Write-Verbose
        Get-ChildItem $PackageDir*.whl `
        | ForEach-Object {
            "Installing $_.Name" | Write-Verbose
            pip install --verbose --verbose $_.Name
        }
    Pop-Location
}

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

if (-not $Env:PYTHON_OUTDIR) {
    "" | Write-Host
    "== Environment variable $Env:PYTHON_OUTDIR is not set. " | Write-Host
    "== We will install $PackageDir from source." | Write-Host
    "" | Write-Host

    Install-FromSource

    "" | Write-Host
    "== $PackageDir installed from source. ==" | Write-Host
    "" | Write-Host
} elseif (-not (Test-Path $Env:PYTHON_OUTDIR)) {
    "" | Write-Warning
    "== The environment variable PYTHON_OUTDIR is set, but pointing to an invalid location ($Env:PYTHON_OUTDIR)" | Write-Warning
    "== To use build artifacts, download the artifacts locally and point the variable to this folder." | Write-Warning
    "" | Write-Warning
    Exit 1
} else {
    "== Preparing environment to use artifacts with version '$Env:PYTHON_VERSION' " | Write-Host
    "== from '$Env:PYTHON_OUTDIR'" | Write-Host
    
    Install-FromBuild
    
    "" | Write-Host
    "== $PackageDir installed from build artifacts. ==" | Write-Host
    "" | Write-Host
}
