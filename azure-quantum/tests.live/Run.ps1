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

function PyTestMarkString() {
    param (
        [string[]] $AzureQuantumCapabilities
    )
    $MarkString = "";
    if ($AzureQuantumCapabilities -contains "submit.ionq") {
        $MarkString += " ionq"
    }
    if ($AzureQuantumCapabilities -contains "submit.honeywell") {
        $MarkString += " honeywell"
    }
    if ($AzureQuantumCapabilities -contains "submit.1qbit") {
        $MarkString += " oneqbit"
    }
    if ($AzureQuantumCapabilities -contains "submit.toshiba") {
        $MarkString += " toshiba"
    }
}

# Copy unit tests without recordings and run Pytest
Copy-Item -Path (Join-Path $PackageDir "tests" "unit" "*.py") -Destination $PSScriptRoot;
if (Test-Path Env:AZURE_QUANTUM_CAPABILITIES) {
    Write-Host "##[info]Using AZURE_QUANTUM_CAPABILITIES env variable: $Env:AZURE_QUANTUM_CAPABILITIES"
    $AzureQuantumCapabilities = $Env:AZURE_QUANTUM_CAPABILITIES -Split ";" | ForEach-Object { $_.trim() }
    # Create marks based on capabilities in test environment
    $MarkString = PyTestMarkString -AzureQuantumCapabilities $AzureQuantumCapabilities;
} else {
    Write-Host "##[info]Missing AZURE_QUANTUM_CAPABILITIES env variable. Will run all live tests."
    $MarkString = "livetest"
}

python -m pytest --junitxml=junit/test-results.xml -v -m $MarkString
