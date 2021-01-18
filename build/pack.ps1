# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
param ([string] $envName, [string] $pkgDir, [string] $outDir)

if ($envName -eq "") {
  Write-Host "##[info]No envName. Setting to default 'qdk'."
  $envName = "qdk"
}

if ($pkgDir -eq "") {
  Write-Host "##[info]No pkgDir. Setting to envName '$envName'"
  $pkgDir = $envName
}

if ($pythonOutDir -eq "") {
  Write-Host "##[info]No outDir. Setting to env var $Env:PYTHON_OUTDIR"
  $outDir = $Env:PYTHON_OUTDIR
}

function PackWheel() {
    param(
        [string] $PenvName,
        [string] $Path,
        [string] $PoutDir
    );

    Push-Location $Path
        sh $PSScriptRoot/pack.sh $PenvName

        if  ($LastExitCode -ne 0) {
            Write-Host "##vso[task.logissue type=error;]Failed to build $Path."
            $script:all_ok = $False
        } else {
            if ($PoutDir -ne "") { 
              Write-Host "##[info]Copying wheel to '$PoutDir'"
              Copy-Item "dist/*.whl" $PoutDir/
              Copy-Item "dist/*.tar.gz" $PoutDir/
            }
        }
    Pop-Location
}

if ($Env:ENABLE_PYTHON -eq "false") {
    Write-Host "##vso[task.logissue type=warning;]Skipping Creating Python packages. Env:ENABLE_PYTHON was set to 'false'."
} else {
    python --version
    $parentPath = Split-Path -parent $PSScriptRoot
    $AbsPkgDir = Join-Path $parentPath $pkgDir
    Write-Host "##[info]Packing Python wheel in env '$envName' for '$AbsPkgDir' to '$outDir'..."
    PackWheel -PenvName $envName -Path $AbsPkgDir -PoutDir $outDir
}
