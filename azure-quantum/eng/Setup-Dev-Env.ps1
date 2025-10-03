# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

try
{
    Push-Location (Join-Path $PSScriptRoot "../")
 
    # Create virtual environment if it doesn't exist
    $VenvPath = "venv"
    if (-not (Test-Path $VenvPath)) {
        Write-Host "Creating virtual environment..."
        python -m venv $VenvPath
    }

    # Activate virtual environment
    Write-Host "Activating virtual environment..."
    & ".\$VenvPath\Scripts\Activate.ps1"

    # Upgrade pip and install build tools
    Write-Host "Upgrading pip and installing build tools..."
    python -m pip install --upgrade pip setuptools wheel

    # Install package in editable mode with optional dependencies
    Write-Host "Installing package in editable mode..."
    pip install -e .[qiskit,cirq,qsharp,dev]
    
    Write-Host ""
    Write-Host "Development environment setup complete!"
    Write-Host "To install additional optional dependencies later, run:"
    Write-Host "  pip install -e .[pulser,quil]  # for specific providers"
    Write-Host "  pip install -e .[all]                 # for all providers (requires Rust toolchain)"
}
finally
{
    Pop-Location
}
