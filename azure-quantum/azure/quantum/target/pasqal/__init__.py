"""Defines targets and helper functions for the Pasqal provider"""

##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

__all__ = [
    "InputParams",
    "Result",
    "Pasqal",
    "PasqalTarget",
]

from .result import Result
from .target import InputParams, Pasqal, PasqalTarget
