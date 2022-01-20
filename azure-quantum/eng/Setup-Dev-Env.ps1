# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

try
{
    Push-Location (Join-Path $PSScriptRoot "../")
 
    conda env create -f environment.yml
    conda env update -f environment.yml --prune
    conda activate azurequantum

    pip install -e .[qiskit,cirq]
}
finally
{
    Pop-Location
}
