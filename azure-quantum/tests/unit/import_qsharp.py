##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import os
import warnings
import pytest


qsharp_installed = False
try:
    # change path to the test folder so that it
    # can correctly import the .qs files
    # when IQ# initializes
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f'Attempting to import qsharp. Current folder: {os.path.curdir}')
    import qsharp
    from qsharp import __version__
    print(f'qsharp {__version__} imported!')
    print(qsharp.component_versions())
    qsharp_installed = True
except ImportError as ex:
    warnings.warn(f"Failed to import `qsharp` with error: {ex.msg}", source=ex)
except Exception as ex:
    warnings.warn(f"Failed to import `qsharp` with error: {ex}", source=ex)

skip_if_no_qsharp = pytest.mark.skipif(not qsharp_installed, reason="Test requires qsharp and IQ# kernel installed.")
