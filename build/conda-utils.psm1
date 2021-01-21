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

    if (Test-CondaEnabled) {
        Write-Host "##[info]Conda is enabled."
        return $true;
    }

    Write-Host "##[info]Enabling conda powershell hook"
    $condahook = (& conda "shell.powershell" "hook") | Out-String
    Write-Host "##[info]Running: $condahook"
    $condahook | Invoke-Expression;
}

function ActivateCondaEnv {
    param (
        [string] $EnvName
    )
    & conda activate $EnvName
    Write-Host "##[info]Activated Conda env: $(Get-PythonConfiguration | Out-String)"
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
