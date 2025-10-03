# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        PowerShell utilities for managing Python virtual environments
#>

function Get-VenvName {
    <#
    .SYNOPSIS
        Get the virtual environment name for a package
    .PARAMETER PackageName
        The name of the package
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string] $PackageName
    )
    
    if ([string]::IsNullOrEmpty($PackageName) -or ($PackageName -eq "azure-quantum")) {
        return "venv"
    }
    return "venv-$PackageName"
}

function New-VenvForPackage {
    <#
    .SYNOPSIS
        Create a new virtual environment for the specified package
    .PARAMETER PackageName
        The name of the package
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string] $PackageName
    )
    
    $VenvName = Get-VenvName -PackageName $PackageName
    $VenvPath = Join-Path (Get-Location) $VenvName
    
    Write-Host "Creating virtual environment '$VenvName' at '$VenvPath'..."
    
    # Create virtual environment if it doesn't exist
    if (-not (Test-Path $VenvPath)) {
        python -m venv $VenvPath
        Write-Host "Virtual environment '$VenvName' created successfully."
    } else {
        Write-Host "Virtual environment '$VenvName' already exists."
    }
    
    # Activate the environment
    Use-Venv -VenvName $VenvName
    
    # Upgrade pip
    Write-Host "Upgrading pip..."
    python -m pip install --upgrade pip setuptools wheel
}

function Use-Venv {
    <#
    .SYNOPSIS
        Activate the specified virtual environment
    .PARAMETER VenvName
        The name of the virtual environment to activate
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string] $VenvName
    )
    
    $VenvPath = Join-Path (Get-Location) $VenvName
    $ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
    
    if (Test-Path $ActivateScript) {
        Write-Host "Activating virtual environment '$VenvName'..."
        # Ensure prompt function exists to avoid activation errors
        if (-not (Get-Command prompt -ErrorAction SilentlyContinue)) {
            function prompt { "PS $($executionContext.SessionState.Path.CurrentLocation)$('>' * ($nestedPromptLevel + 1)) " }
        }
        & $ActivateScript
    } else {
        Write-Warning "Virtual environment '$VenvName' not found at '$VenvPath'. Trying to use current Python environment."
    }
}

function Install-PackageInVenv {
    <#
    .SYNOPSIS
        Install a package in the current virtual environment
    .PARAMETER PackageName
        The name of the package to install
    .PARAMETER FromSource
        Whether to install from source (editable install)
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string] $PackageName,
        
        [Parameter(Mandatory=$false)]
        [bool] $FromSource = $false
    )
    
    if ($FromSource) {
        Write-Host "Installing '$PackageName' from source (editable install)..."
        pip install -e ".$PackageName"
    } else {
        Write-Host "Installing '$PackageName' from PyPI..."
        pip install $PackageName
    }
}

# Export functions
Export-ModuleMember -Function Enable-Venv, Get-VenvName, New-VenvForPackage, Use-Venv, Install-PackageInVenv