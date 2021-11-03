# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Includes utility cmdlets for working with conda both locally,
        and in Azure Pipelines and other hosted environments.
#>

function Test-CondaEnabled {
    <#
        .SYNOPSIS
            Tests if conda has been enabled for shell
            use (e.g.: if conda activate will work).
    #>

    # The shell hook for conda creates a new cmdlet called
    # Invoke-Conda that is then aliased to `conda`. If the
    # full name (without an alias) is available, then the hook
    # has been run already.
    if ($null -ne (Get-Command Invoke-Conda -ErrorAction SilentlyContinue)) {
        return $true;
    }
    return $false;
}

function Enable-Conda {
    <#
        .SYNOPSIS
            Attempts to enable conda for shell usage, first using
            the CONDA environment variable for the path, falling back
            to PATH, and then failing.
            If conda is already enabled, this cmdlet does nothing,
            so that this cmdlet is idempotent.
    #>

    if (Test-CondaEnabled) { return $true; }

    if ("$Env:CONDA" -ne "") {
        # Try and run the shell hook from the path nominated
        # by CONDA.

        # On Windows, this is $Env:CONDA/Scripts/conda.exe, while on
        # Linux and macOS, this is $Env:CONDA/bin/conda.

        if ($IsWindows) {
            $condaBin = Join-Path $Env:CONDA "Scripts" "conda.exe";
        } else {
            $condaBin = Join-Path $Env:CONDA "bin" "conda";
        }

        if ($null -eq (Get-Command $condaBin -ErrorAction SilentlyContinue)) {
            Write-Error "##[error] conda binary was expected at $condaBin (CONDA = $Env:CONDA), but was not found.";
            throw;
        }

        (& $condaBin shell.powershell hook) | Out-String | Invoke-Expression;
    } else {
        (conda shell.powershell hook) | Out-String | Invoke-Expression;
    }
}

function Use-CondaEnv {
    param (
        [string] $EnvName
    )
    <#
        .SYNOPSIS
            Activates a conda environment, reporting the new configuration
            after having done so. If conda has not already been enabled, this
            cmdlet will enable it before activating.
    #>

    Enable-Conda
    # NB: We use the PowerShell cmdlet created by the conda shell hook here
    #     to avoid accidentally using the conda binary.
    Enter-CondaEnvironment $EnvName
    Write-Host "##[info]Activated Conda env: $(Get-PythonConfiguration | Out-String)"
}

function Install-Package() {
    param(
      [string] $EnvName,
      [string] $PackageName,
      [bool] $FromSource
    )
    # Activate env
    Use-CondaEnv $EnvName
    # Install package
    if ($True -eq $FromSource) {
      $ParentPath = Split-Path -parent $PSScriptRoot
      $AbsPackageDir = Join-Path $ParentPath $PackageName
      Write-Host "##[info]Install package $AbsPackageDir in development mode for env $EnvName"
      pip install -e $AbsPackageDir
    } else {
      Write-Host "##[info]Install package $PackageName for env $EnvName"
      pip install $PackageName
    }
}

function Get-PythonConfiguration {
    <#
        .SYNOPSIS
            Returns a table describing the current Python configuration,
            useful for diagnostic purposes.
    #>

    $table = @{};

    $python = (Get-Command python -ErrorAction SilentlyContinue);
    if ($null -ne $python) {
        $table["PythonLocation"] = $python.Source;
        try {
            $table["PythonVersion"] = & $python --version;
        } catch { }
    }

    # If the CONDA environment variable is set, allow that to override
    # the local PATH.
    $conda = Get-Command conda -ErrorAction SilentlyContinue;

    if ($null -ne $conda) {
        $table["CondaLocation"] = $conda.Source;
        try {
            $table["CondaVersion"] = & $conda --version;
        } catch { }
    }

    # If the conda hook has already been run, we can get some additional
    # information for the table.
    if (Test-CondaEnabled) {
        try {
            $env = Get-CondaEnvironment | Where-Object -Property Active;
            if ($null -ne $env) {
                $table["CondaEnvName"] = $env.Name;
                $table["CondaEnvPath"] = $env.Path;
            }
        } catch { }
    }

    $table | Write-Output;
}
