# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Pack: create wheels for given packages in given environments, output to directory
#>

param (
  [string] $PackageDir,
  [string] $OutDir
)

& (Join-Path $PSScriptRoot "set-env.ps1");

Import-Module (Join-Path $PSScriptRoot "conda-utils.psm1");

if ('' -eq $PackageDir) {
  # If no package dir is specified, find all packages that contain an environment.yml file
  $parentPath = Split-Path -parent $PSScriptRoot
  $PackageDirs = Get-ChildItem -Path $parentPath -Recurse -Filter "environment.yml" | Select-Object -ExpandProperty Directory | Split-Path -Leaf
  Write-Host "##[info]No PackageDir. Setting to default '$PackageDirs'"
} else {
  $PackageDirs = @($PackageDir);
}

if ($OutDir -eq "") {
  Write-Host "##[info]No OutDir. Setting to env var $Env:PYTHON_OUTDIR"
  $OutDir = $Env:PYTHON_OUTDIR
}

$script:all_ok = $True

function Create-Wheel() {
  param(
    [string] $EnvName,
    [string] $Path,
    [string] $OutDir
  );

  Push-Location $Path
    # Set environment vars to be able to run conda activate
    Write-Host "##[info]Pack wheel for env '$EnvName'"
    # Activate env
    Use-CondaEnv $EnvName
    # Create package distribution
    python setup.py bdist_wheel sdist --formats=gztar

    if  ($LastExitCode -ne 0) {
      Write-Host "##vso[task.logissue type=error;]Failed to build $Path."
      $script:all_ok = $False
    } else {
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

    foreach ($PackageDir in $PackageDirs) {
      $EnvName = $PackageDir.replace("-", "")
      $AbsPath = Join-Path $parentPath $PackageDir
      Write-Host "##[info]Packing Python wheel in env '$EnvName' for '$PackageDir' to '$OutDir'..."
      Create-Wheel -EnvName $EnvName -Path $AbsPath -OutDir $OutDir
    }
}
