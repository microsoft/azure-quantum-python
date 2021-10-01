# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

<#
    .SYNOPSIS
        Pack: create wheels for given packages in given environments, output to directory
#>

param (
  [string] $PackageName,
  [string] $OutDir
)

& (Join-Path $PSScriptRoot "set-env.ps1");

Import-Module (Join-Path $PSScriptRoot "package-utils.psm1");

if ($OutDir -eq "") {
  Write-Host "##[info]No OutDir. Setting to env var $Env:PYTHON_OUTDIR"
  $OutDir = $Env:PYTHON_OUTDIR
}

$script:all_ok = $True

if ($Env:ENABLE_PYTHON -eq "false") {
    Write-Host "##vso[task.logissue type=warning;]Skipping Creating Python packages. Env:ENABLE_PYTHON was set to 'false'."
} else {
    python --version
    $parentPath = Split-Path -parent $PSScriptRoot
    $PackageNames = PackagesList -PackageName $PackageName

    foreach ($PackageName in $PackageNames) {
      $EnvName = $PackageName.replace("-", "")
      $AbsPath = Join-Path $parentPath $PackageName
      Write-Host "##[info]Packing Python wheel in env '$EnvName' for '$PackageName' to '$OutDir'..."
      New-Wheel -EnvName $EnvName -Path $AbsPath -OutDir $OutDir
    }
}
