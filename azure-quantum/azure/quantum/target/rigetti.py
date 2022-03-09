"""Defines targets and helper functions for the Rigetti provider"""

##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

__all__ = [
    "Readout",
    "Result",
    "Rigetti",
    "RigettiTarget",
]

import json
from enum import Enum
from typing import Union, Dict, List, TypeVar, Generic, cast

from .target import Target
from ..job import Job
from ..workspace import Workspace


class RigettiTarget(str, Enum):
    """The known targets for the Rigetti provider

    See https://qcs.rigetti.com/qpus for details on a QPU target.
    """

    QVM = "rigetti.qvm"
    """A simulator target for Quil. See https://github.com/quil-lang/qvm for more info."""

    ASPEN_11 = "rigetti.aspen-11"
    ASPEN_M_1 = "rigetti.aspen-m-1"


class Rigetti(Target):
    """Rigetti target, defaults to the simulator RigettiTarget.QVM

    In order to process the results of a Quil input to this target, we recommend using the included Result class.
    """

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


RawData = Union[int, float, List[float]]


class Result:
    """Downloads the data of a completed Job and extracts the readout values in the correct type."""

    def __init__(self, job: Job) -> None:
        """Decode the results of a Job into a RigettiResult"""

        data = cast(Dict[str, List[List[RawData]]], json.loads(job.download_data(job.details.output_data_uri)))
        self.data_per_register: Dict[str, Readout] = {k: Readout(v) for k, v in data.items()}

    def __getitem__(self, register_name: str) -> "Readout":
        return self.data_per_register[register_name]


T = TypeVar("T", bound=Union[int, float, complex])


class Readout(Generic[T]):
    """Contains the data of a declared "readout" memory region, usually the ``ro`` register.

    All data for all shots for a single Readout will have the same datatype T corresponding to the declared Quil data type:

    * ``BIT`` | ``OCTET`` | ``INTEGER``: ``int``
    * ``REAL``: ``float``
    """

    def __init__(self, raw_data: List[List[RawData]]) -> None:
        if isinstance(raw_data[0][0], list):
            raw_data = [[complex(entry[0], entry[1]) for entry in shot] for shot in raw_data]

        self.data_per_shot: List[List[T]] = raw_data

    def __getitem__(self, shot: int) -> List[T]:
        return self.data_per_shot[shot]
