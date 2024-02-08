##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import os
import warnings
import pytest
from importlib.metadata import version, PackageNotFoundError

qsharp_installed = False
try:
    # change path to the test folder so that it
    # can correctly import the .qs files
    # when Q# initializes
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f'Attempting to import qsharp. Current folder: {os.path.curdir}')

    qsharp_version = version("qsharp")
    print(f'qsharp v{qsharp_version} was successfully imported!')

    import qsharp
    qsharp.init(target_profile=qsharp.TargetProfile.Base)
    print(f'Base Q# Profile has been successfully initialized.')
    qsharp_installed = True
except PackageNotFoundError as ex:
    warnings.warn(f"`qsharp` package was not found. Make sure it's installed.", source=ex)
except Exception as ex:
    warnings.warn(f"Failed to import `qsharp` with error: {ex}", source=ex)

skip_if_no_qsharp = pytest.mark.skipif(not qsharp_installed, reason="Test requires qsharp and IQ# kernel installed.")
