# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
function PackWheel() {
    param(
        [string] $Path
    );

    Push-Location (Join-Path $PSScriptRoot $Path)
        source activate qdk
        python setup.py bdist_wheel sdist --formats=gztar

        if  ($LastExitCode -ne 0) {
            Write-Host "##vso[task.logissue type=error;]Failed to build $Path."
            $script:all_ok = $False
        } else {
            Copy-Item "dist/*.whl" $Env:PYTHON_OUTDIR
            Copy-Item "dist/*.tar.gz" $Env:PYTHON_OUTDIR
        }
    Pop-Location
}

if ($Env:ENABLE_PYTHON -eq "false") {
    Write-Host "##vso[task.logissue type=warning;]Skipping Creating Python packages. Env:ENABLE_PYTHON was set to 'false'."
} else {
    Write-Host "##[info]Packing Python wheel..."
    python --version
    # PackWheel '../qdk'
}
