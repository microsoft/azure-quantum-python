# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Pack: create wheels for given packages in given environments, output to directory
#>

param (
  [string[]] $PackageDirs,
  [string[]] $EnvNames,
  [string] $OutDir
)

& (Join-Path $PSScriptRoot "set-env.ps1");

Import-Module (Join-Path $PSScriptRoot "conda-utils.psm1");

if ($null -eq $PackageDirs) {
  $parentPath = Split-Path -parent $PSScriptRoot
  $PackageDirs = Get-ChildItem -Path $parentPath -Recurse -Filter "environment.yml" | Select-Object -ExpandProperty Directory | Split-Path -Leaf
  Write-Host "##[info]No PackageDir. Setting to default '$PackageDirs'"
}

if ($null -eq $EnvNames) {
  $EnvNames = $PackageDirs | ForEach-Object {$_.replace("-", "")}
  Write-Host "##[info]No EnvNames. Setting to default '$EnvNames'"
}

if ($OutDir -eq "") {
  Write-Host "##[info]No OutDir. Setting to env var $Env:PYTHON_OUTDIR"
  $OutDir = $Env:PYTHON_OUTDIR
}

# Check that input is valid
if ($EnvNames.length -ne $PackageDirs.length) {
  throw "Cannot run build script: '$EnvNames' and '$PackageDirs' lengths don't match"
}

function Create-Wheel() {
  param(
    [string] $EnvName,
    [string] $Path,
    [string] $OutDir
  );

  Push-Location $Path
    # Set environment vars to be able to run conda activate
    Enable-Conda
    Write-Host "##[info]Pack wheel for env '$EnvName'"
    # Activate env
    ActivateCondaEnv $EnvName
    # Create package distribution
    python setup.py bdist_wheel sdist --formats=gztar

    if  ($LastExitCode -ne 0) {
      Write-Host "##vso[task.logissue type=error;]Failed to build $Path."
      $script:all_ok = $False
    } else {
      $script:all_ok = $True
      if ($OutDir -ne "") { 
        Write-Host "##[info]Copying wheel to '$OutDir'"
        Copy-Item "dist/*.whl" $OutDir/
        Copy-Item "dist/*.tar.gz" $OutDir/
      }
    }
  Pop-Location
}

if ($Env:ENABLE_PYTHON -eq "false") {
    Write-Host "##vso[task.logissue type=warning;]Skipping Creating Python packages. Env:ENABLE_PYTHON was set to 'false'."
} else {
    python --version
    $parentPath = Split-Path -parent $PSScriptRoot

    for ($i=0; $i -le $PackageDirs.length-1; $i++) {
      $PackageDir = Join-Path $parentPath $PackageDirs[$i]
      Write-Host "##[info]Packing Python wheel in env '$EnvNames[$i]' for '$PackageDir' to '$OutDir'..."
      Create-Wheel -EnvName $EnvNames[$i] -Path $PackageDir -OutDir $OutDir
    }
}
