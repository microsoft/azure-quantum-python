# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# Sometimes another package may create a requirement of that the azure-quantum
# package is within a particular version.
# But when installing locally (via pip install and setup.py), the default version will be 0.0.1.
# One can set the PYTHON_VERSION environment variable (used in setup.py)
# or use this script to automatically set it to the latest published version.
# 
# If you still get conflicts when doing a pip install, please set the 
# PYTHON_VERSION environment variable to a version that matches the other packages' contraints.

$VerbosePreference = 'Continue'

if (-not "$env:PYTHON_VERSION") 
{
    # attempt to get the latest published version by calling pip install on an invalid version
    $pipInstallResult = $(pip install azure_quantum==invalid *>&1) | Out-String
    $getLatestVersionRegex = '(?:\(from\sversions:)(?:(?:\s|,)*(\d+\.\d+\.\d+(?:\.\d+)?(?:b\d+)?))+\)'
    if ($pipInstallResult -match $getLatestVersionRegex) 
    {
        Write-Verbose "Setting PYTHON_VERSION env var to latest published version of azure-quantum: $($Matches[1])"
        $env:PYTHON_VERSION = $Matches[1]
    }
}
