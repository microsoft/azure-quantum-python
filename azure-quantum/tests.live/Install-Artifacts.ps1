# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Install-Artifacts: set up a Python environment using Anaconda
#>

$PackageDir = Split-Path -parent $PSScriptRoot;
$RootDir = Split-Path -parent $PackageDir;
Import-Module (Join-Path $RootDir "build" "conda-utils.psm1");
Import-Module (Join-Path $RootDir "build" "package-utils.psm1");

# Enable conda hook
Enable-Conda

NewCondaEnvForPackage -PackageName $PackageDir

if (-not $Env:PYTHON_OUTDIR) {
    "" | Write-Host
    "== Environment variable $Env:PYTHON_OUTDIR is not set. " | Write-Host
    "== We will install $PackageDir from source." | Write-Host
    "" | Write-Host

    Install-PackageInEnv -PackageName $PackageDir -FromSource $FromSource

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
    
    Install-PackageInEnv -PackageName $PackageDir -FromSource $False -BuildArtifactPath $Env:PYTHON_OUTDIR
    
    "" | Write-Host
    "== $PackageDir installed from build artifacts. ==" | Write-Host
    "" | Write-Host
}
