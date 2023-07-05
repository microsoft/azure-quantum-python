# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Test: Run unit tests for given packages/environments
#>

param (
  [bool] $SkipInstall
)

# For debug, print all relevant environment variables:
Get-ChildItem env:AZURE*, env:*VERSION, env:*OUTDIR | Format-Table | Out-String | Write-Host

$PackageDir = Split-Path -parent $PSScriptRoot;
$PackageName = $PackageDir | Split-Path -Leaf;
$RootDir = Split-Path -parent $PackageDir;
Import-Module (Join-Path $RootDir "build" "conda-utils.psm1");
Import-Module (Join-Path $RootDir "build" "package-utils.psm1");

if ($True -eq $SkipInstall) {
    Write-Host "##[info]Skipping install."
} else {
    & (Join-Path $PSScriptRoot Install-Artifacts.ps1)
}

Enable-Conda

# Try installing IQ# dotnet tool, IQ# kernel and the qsharp Python package
# Used for running tests between the Azure Quantum Python SDK and IQ# (Q#+QIR job submission)
if ([string]::IsNullOrEmpty($PackageName) -or ($PackageName -eq "azure-quantum")) {
    try {
      $EnvExists = conda env list | Select-String -Pattern "azurequantum " | Measure-Object | Select-Object -Exp Count
      if ($EnvExists) {
        conda activate azurequantum
        If ($null -eq $Env:TOOLS_DIR) { $Env:TOOLS_DIR =  [IO.Path]::GetFullPath((Join-Path $RootDir ".tools")) }
        If (-not (Test-Path -Path $Env:TOOLS_DIR)) { [IO.Directory]::CreateDirectory($Env:TOOLS_DIR) }
        & (Join-Path $RootDir "build" "install-iqsharp.ps1");
      }    
    }
    catch {
      Write-Host "##[warning]Failed to install IQ#."
    }
}

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
    if ($AzureQuantumCapabilities -notcontains "submit.toshiba") {
        $MarkExpr += " and not toshiba"
    }
    if ($AzureQuantumCapabilities -notcontains "submit.rigetti") {
        $MarkExpr += " and not rigetti"
    }
    if ($AzureQuantumCapabilities -notcontains "submit.quantinuum") {
        $MarkExpr += " and not quantinuum"
    }
    if ($AzureQuantumCapabilities -notcontains "submit.microsoft-qc") {
        $MarkExpr += " and not microsoft_qc"
    }

    return $MarkExpr
}

if (Test-Path Env:AZURE_QUANTUM_CAPABILITIES) {
    Write-Host "##[info]Using AZURE_QUANTUM_CAPABILITIES env variable: $Env:AZURE_QUANTUM_CAPABILITIES"
    $AzureQuantumCapabilities = $Env:AZURE_QUANTUM_CAPABILITIES -Split ";" | ForEach-Object { $_.trim().ToLower() }
    # Create marks based on capabilities in test environment
    $MarkExpr = PyTestMarkExpr -AzureQuantumCapabilities $AzureQuantumCapabilities;
} else {
    Write-Host "##[info]Missing AZURE_QUANTUM_CAPABILITIES env variable. Will run all live tests."
    $MarkExpr = "live_test"
}

pip install pytest | Write-Host

$logs = Join-Path $env:BUILD_ARTIFACTSTAGINGDIRECTORY "logs" "qdk-python.txt"
" ==> Generating logs to $logs" | Write-Host

# Copy unit tests without recordings and run Pytest
Write-Host "##[info]Copy unit test files from $PackageDir to $PSScriptRoot"
Copy-Item -Path (Join-Path $PackageDir "tests" "unit" "*.py") -Destination $PSScriptRoot
if ($PackageDir -Match "azure-quantum") {
    Write-Host "##[info]Copy auxiliary bitcode files from $PackageDir to $PSScriptRoot/qir"
    New-Item -ItemType Directory -Path $PSScriptRoot -Name qir
    # Copies auxiliary bitcode files that are used by unit tests in azure_quantum
    Copy-Item -Path (Join-Path $PackageDir "tests" "unit" "qir" "*.bc") -Destination (Join-Path $PSScriptRoot "qir")

    Write-Host "##[info]Copy auxiliary Q# test files from $PackageDir to $PSScriptRoot"
    Copy-Item -Path (Join-Path $PackageDir "tests" "unit" "*.qs") -Destination $PSScriptRoot
}

python -m pytest -v `
    --junitxml=junit/test-results.xml `
    --log-level=INFO `
    --log-file-format="%(asctime)s %(levelname)s %(message)s" `
    --log-file=$logs `
    -m $MarkExpr 
