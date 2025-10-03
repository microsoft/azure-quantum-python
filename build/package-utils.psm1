# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        PowerShell utilities for package management
#>

function Install-PackageInEnv {
    <#
    .SYNOPSIS
        Install a package in the current environment
    .PARAMETER PackageName
        The name of the package to install
    .PARAMETER FromSource
        Whether to install from source (editable install)
    .PARAMETER BuildArtifactPath
        Path to build artifacts (optional)
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string] $PackageName,
        
        [Parameter(Mandatory=$false)]
        [bool] $FromSource = $false,
        
        [Parameter(Mandatory=$false)]
        [string] $BuildArtifactPath = ""
    )
    
    if ($FromSource) {
        Write-Host "Installing '$PackageName' from source (editable install)..."
        $ParentPath = Split-Path -parent $PSScriptRoot
        $AbsPackageName = Join-Path $ParentPath $PackageName
        Write-Host "##[info]Install package $AbsPackageName in development mode for env $EnvName"
        pip install -e $AbsPackageName
    } elseif (-not [string]::IsNullOrEmpty($BuildArtifactPath)) {
        Write-Host "Installing '$PackageName' from build artifacts at '$BuildArtifactPath'..."
        $WheelFiles = Get-ChildItem -Path $BuildArtifactPath -Filter "*.whl"
        if ($WheelFiles.Count -gt 0) {
            pip install $WheelFiles[0].FullName
        } else {
            Write-Warning "No wheel files found in '$BuildArtifactPath'. Installing from PyPI instead."
            pip install $PackageName
        }
    } else {
        Write-Host "Installing '$PackageName' from PyPI..."
        pip install $PackageName
    }
}

# Export functions
Export-ModuleMember -Function Install-PackageInEnv