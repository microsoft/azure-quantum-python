# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Test: Run unit tests for given packages/environments
#>

param (
  [bool] $SkipInstall
)

$PackageDir = Split-Path -parent $PSScriptRoot;
$PackageName = $PackageDir | Split-Path -Leaf;
$RootDir = Split-Path -parent $PackageDir;
Import-Module (Join-Path $RootDir "build" "conda-utils.psm1");

if ($True -eq $SkipInstall) {
    Write-Host "##[info]Skipping install."
} else {
    & (Join-Path $PSScriptRoot Install-Artifacts.ps1)
}

# Activate env
$EnvName = GetEnvName -PackageName $PackageName
Use-CondaEnv $EnvName

function PyTestMarkExpr() {
    param (
        [string[]] $AzureQuantumCapabilities
    )
    $MarkExpr = "live_test";
    if ($AzureQuantumCapabilities -notcontains "submit.ionq") {
        $MarkExpr += " and not ionq"
    }
    if ($AzureQuantumCapabilities -notcontains "submit.honeywell") {
        $MarkExpr += " and not honeywell"
    }
    if ($AzureQuantumCapabilities -notcontains "submit.1qbit") {
        $MarkExpr += " and not oneqbit"
    }
    if ($AzureQuantumCapabilities -notcontains "submit.toshiba") {
        $MarkExpr += " and not toshiba"
    }
    if ($AzureQuantumCapabilities -notcontains "submit.microsoft") {
        $MarkExpr += " and not qio"
    }

    return $MarkExpr
}

# Copy unit tests without recordings and run Pytest
Copy-Item -Path (Join-Path $PackageDir "tests" "unit" "*.py") -Destination $PSScriptRoot;
Copy-Item -Path (Join-Path $PackageDir "tests" "unit" "aio" "*.py") -Destination $PSScriptRoot;
Copy-Item -Path (Join-Path $PackageDir "tests" "unit" "conftest.py") -Destination $PSScriptRoot;
if (Test-Path Env:AZURE_QUANTUM_CAPABILITIES) {
    Write-Host "##[info]Using AZURE_QUANTUM_CAPABILITIES env variable: $Env:AZURE_QUANTUM_CAPABILITIES"
    $AzureQuantumCapabilities = $Env:AZURE_QUANTUM_CAPABILITIES -Split ";" | ForEach-Object { $_.trim().ToLower() }
    # Create marks based on capabilities in test environment
    $MarkExpr = PyTestMarkExpr -AzureQuantumCapabilities $AzureQuantumCapabilities;
} else {
    Write-Host "##[info]Missing AZURE_QUANTUM_CAPABILITIES env variable. Will run all live tests."
    $MarkExpr = "live_test"
}

python -m pytest --junitxml=junit/test-results.xml -v -m $MarkExpr
