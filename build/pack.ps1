# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
param (
  [string[]] $envNames,
  [string[]] $pkgDirs,
  [string] $outDir
)

if ($null -eq $pkgDirs) {
  $parentPath = Split-Path -parent $PSScriptRoot
  $pkgDirs = Get-ChildItem -Path $parentPath -Recurse -Filter "environment.yml" | Select-Object -ExpandProperty Directory | Split-Path -Leaf
  Write-Host "##[info]No pkgDir. Setting to default '$pkgDirs'"
}

if ($null -eq $envNames) {
  $envNames = $pkgDirs | ForEach-Object {$_.replace("-","")}
  Write-Host "##[info]No envNames. Setting to default '$envNames'"
}

if ($outDir -eq "") {
  Write-Host "##[info]No outDir. Setting to env var $Env:PYTHON_OUTDIR"
  $outDir = $Env:PYTHON_OUTDIR
}

function PackWheel() {
  param(
    [string] $envName,
    [string] $Path,
    [string] $outDir
  );

  Push-Location $Path
    # Set environment vars to be able to run conda activate
    (& conda "shell.powershell" "hook") | Out-String | Invoke-Expression
    Write-Host "##[info]Pack wheel for env '$envName'"
    # Activate env
    conda activate $envName
    which python
    # Create package distribution
    python setup.py bdist_wheel sdist --formats=gztar

    if  ($LastExitCode -ne 0) {
      Write-Host "##vso[task.logissue type=error;]Failed to build $Path."
      $script:all_ok = $False
    } else {
      if ($outDir -ne "") { 
        Write-Host "##[info]Copying wheel to '$outDir'"
        Copy-Item "dist/*.whl" $outDir/
        Copy-Item "dist/*.tar.gz" $outDir/
      }
    }
  Pop-Location
}

if ($Env:ENABLE_PYTHON -eq "false") {
    Write-Host "##vso[task.logissue type=warning;]Skipping Creating Python packages. Env:ENABLE_PYTHON was set to 'false'."
} else {
    python --version
    $parentPath = Split-Path -parent $PSScriptRoot

    for ($i=0; $i -le $pkgDirs.length-1; $i++) {
      $AbsPkgDir = Join-Path $parentPath $pkgDirs[$i]
      Write-Host "##[info]Packing Python wheel in env '$envNames[$i]' for '$AbsPkgDir' to '$outDir'..."
      PackWheel -envName $envNames[$i] -Path $AbsPkgDir -outDir $outDir
    }
}
