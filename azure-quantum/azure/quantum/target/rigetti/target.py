"""Defines targets and helper functions for the Rigetti provider"""

##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

__all__ = [
    "Rigetti",
    "RigettiTarget",
]

from enum import Enum
from typing import Union

from ..target import Target
from ...workspace import Workspace


class RigettiTarget(str, Enum):
    """The known targets for the Rigetti provider

    See https://qcs.rigetti.com/qpus for details on a QPU target.
    """

    QVM = "rigetti.sim.qvm"
    """A simulator target for Quil. See https://github.com/quil-lang/qvm for more info."""

    ASPEN_11 = "rigetti.qpu.aspen-11"
    ASPEN_M_1 = "rigetti.qpu.aspen-m-1"


class Rigetti(Target):
    """Rigetti target, defaults to the simulator RigettiTarget.QVM

    In order to process the results of a Quil input to this target, we recommend using the included Result class.
    """

    target_names = tuple(target.value for target in RigettiTarget)

    def __init__(
            self,
            workspace: Workspace,
            name: Union[RigettiTarget, str] = RigettiTarget.QVM,
            input_data_format: str = "rigetti.quil.v1",
            output_data_format: str = "rigetti.quil-results.v1",
            provider_id: str = "rigetti",
            encoding: str = "",
            **kwargs
    ):
        super().__init__(
            workspace=workspace,
            name=name,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            provider_id=provider_id,
            content_type="text/plain",
            encoding=encoding,
            **kwargs
        )
