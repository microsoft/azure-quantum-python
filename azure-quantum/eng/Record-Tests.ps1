# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# Delete old recordings
$Recordings_Folder =  Join-Path $PSScriptRoot "../tests/unit/recordings/"
if (Test-Path $Recordings_Folder) {
    Remove-Item $Recordings_Folder -Recurse | Write-Verbose
}
# Delete old recordings
$Recordings_Folder =  Join-Path $PSScriptRoot "../tests/unit/aio/recordings/"
if (Test-Path $Recordings_Folder) {
    Remove-Item $Recordings_Folder -Recurse | Write-Verbose
}

pytest
