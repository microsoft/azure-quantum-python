# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

$ErrorActionPreference = 'Stop'

Write-Host "Setting up build environment variables"

If ($null -eq $Env:BUILD_BUILDNUMBER) { $Env:BUILD_BUILDNUMBER = "0.0.1.0" }
If ($null -eq $Env:BUILD_CONFIGURATION) { $Env:BUILD_CONFIGURATION = "Debug"}
If ($null -eq $Env:BUILD_VERBOSITY) { $Env:BUILD_VERBOSITY = "m"}
If ($null -eq $Env:ASSEMBLY_VERSION) { $Env:ASSEMBLY_VERSION = "$Env:BUILD_BUILDNUMBER"}
If ($null -eq $Env:PYTHON_VERSION) { $Env:PYTHON_VERSION = "${Env:ASSEMBLY_VERSION}a1" }

If ($null -eq $Env:DROPS_DIR) { $Env:DROPS_DIR =  [IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\drops")) }

If ($null -eq $Env:PYTHON_OUTDIR) { $Env:PYTHON_OUTDIR =  (Join-Path $Env:DROPS_DIR "wheels") }
If (-not (Test-Path -Path $Env:PYTHON_OUTDIR)) { [IO.Directory]::CreateDirectory($Env:PYTHON_OUTDIR) }

If ($null -eq $Env:ENABLE_PYTHON) { $Env:ENABLE_PYTHON =  "true" }

# Workaround for issue https://github.com/microsoft/qdk-python/issues/220
$RequirementsTxt = Join-Path $PSScriptRoot "../azure-quantum/requirements.txt"
(Get-Content $RequirementsTxt) `
    -replace 'azure-core>=1.21.1', 'azure-core>=1.19.1' |
  Out-File $RequirementsTxt

# Pin urllib3 for compatibility with vcrpy
Add-Content $RequirementsTxt "`nurllib3==1.26.15"
