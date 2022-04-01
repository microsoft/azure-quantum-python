"""Defines targets and helper functions for the Rigetti provider"""

##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

__all__ = [
    "InputParams",
    "Readout",
    "Result",
    "Rigetti",
    "RigettiTarget",
]

from .result import Readout, Result
from .target import InputParams, Rigetti, RigettiTarget
