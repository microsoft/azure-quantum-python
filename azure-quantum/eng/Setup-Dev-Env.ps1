# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

$VerbosePreference = 'Continue'

try
{
    Push-Location (Join-Path $PSScriptRoot "../")
    ./eng/Set-To-Latest-Version.ps1 -Verbose | Write-Verbose

    conda env create -f environment.yml
    conda env update -f environment.yml --prune
    conda activate azurequantum
}
finally
{
    Pop-Location
}
