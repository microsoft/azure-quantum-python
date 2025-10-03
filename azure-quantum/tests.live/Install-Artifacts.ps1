# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Install-Artifacts: set up a Python environment using virtual environments
#>

$PackageDir = Split-Path -parent $PSScriptRoot;
$PackageName = $PackageDir | Split-Path -Leaf;
$RootDir = Split-Path -parent $PackageDir;
Import-Module (Join-Path $RootDir "build" "venv-utils.psm1") -Force;
Import-Module (Join-Path $RootDir "build" "package-utils.psm1") -Force;

New-VenvForPackage -PackageName $PackageName

if (-not $Env:PYTHON_OUTDIR) {
    "" | Write-Host
    "== Environment variable $Env:PYTHON_OUTDIR is not set. " | Write-Host
    "== We will install $PackageName from source." | Write-Host
    "" | Write-Host

    $PackageWithExtras = "$PackageName[qiskit,cirq,qsharp,dev]"
    Install-PackageInEnv -PackageName $PackageWithExtras -FromSource $True

    "" | Write-Host
    "== $PackageName installed from source. ==" | Write-Host
    "" | Write-Host
} elseif (-not (Test-Path $Env:PYTHON_OUTDIR)) {
    "" | Write-Warning
    "== The environment variable PYTHON_OUTDIR is set, but pointing to an invalid location ($Env:PYTHON_OUTDIR)" | Write-Warning
    "== To use build artifacts, download the artifacts locally and point the variable to this folder." | Write-Warning
    "" | Write-Warning
    Exit 1
}

# this condition is used by the E2E Live test pipeline
elseif ($Env:PICK_QDK_VERSION -eq "auto") {
    "== Installing latest published $PackageName package from PyPI..." | Write-Host
    Install-PackageInEnv -PackageName $PackageName -FromSource $False
} else {
    "== Preparing environment to use artifacts with version '$Env:PYTHON_VERSION' " | Write-Host
    "== from '$Env:PYTHON_OUTDIR'" | Write-Host
    if ($Env:PYTHON_VERSION) {
        $NameAndVersion = "$PackageName[qiskit,cirq,qsharp,dev]==$($Env:PYTHON_VERSION)"
    } else {
        $NameAndVersion = "$PackageName[qiskit,cirq,qsharp,dev]"
    }
    
    Install-PackageInEnv -PackageName $NameAndVersion -FromSource $False -BuildArtifactPath $Env:PYTHON_OUTDIR
    
    "" | Write-Host
    "== $PackageName installed from build artifacts. ==" | Write-Host
    "" | Write-Host
}
