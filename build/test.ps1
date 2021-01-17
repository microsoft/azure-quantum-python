# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
param ($envName, $pkgDir)
Write-Host "##[info]Install package $pkgDir in development mode and run tests for env $envName"
Write-Host "##[info]1. Activate $envName"
conda activate $envName
which python
Write-Host "##[info]2. Install $pkgDir, Python: $(which python)"
pip install -e $pkgDir
Write-Host "##[info]3. Run pytest"
pytest $pkgDir
