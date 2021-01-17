# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
param ($envName)
Write-Host "##[info]Install package in development mode and run tests for env $envName"
conda activate $envName
Write-Host "##[info]Installing ($envName), Python: $(which python)"
pip install -e .
Write-Host "##[info]Running pytest"
pytest
