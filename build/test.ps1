# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
param ($envName, $pkgDir)
Write-Host "##[info]Install package $pkgDir in development mode and run tests for env $envName"
conda shell.powershell hook
Write-Host "##[info]Activate $envName"
conda activate $envName
which python
Write-Host "##[info]Installing $pkgDir, Python: $(which python)"
pip install -e $pkgDir
Write-Host "##[info]Running pytest"
pytest $pkgDir
