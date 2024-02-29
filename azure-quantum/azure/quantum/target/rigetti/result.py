"""Defines targets and helper functions for the Rigetti provider"""

##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

__all__ = [
    "Readout",
    "Result",
]

import json
from typing import Union, Dict, List, TypeVar, cast

from ...job import Job

RawData = Union[int, float, List[float]]


class Result:
    """Downloads the data of a completed Job and extracts the ``Readout`` for each register.

    .. highlight:: python
    .. code-block::
       from azure.quantum.job import Job
       from azure.quantum.target.rigetti import Result
       job = Job(...)  # This job should come from a Rigetti target
       job.wait_until_completed()
       result = Result(job)
       ro_data = result["ro"]
       first_shot_data = ro_data[0]
    """

    def __init__(self, job: Job) -> None:
        """
        Decode the results of a Job with output type of "rigetti.quil-results.v1"

        Args:
            job (Job): Azure Quantum job
        Raises:
            RuntimeError: if the job has not completed successfully
        """

        if job.details.status != "Succeeded":
            raise RuntimeError(
                "Cannot retrieve results as job execution failed "
                f"(status: {job.details.status}."
                f"error: {job.details.error_data})"
            )
        data = cast(Dict[str, List[List[RawData]]], json.loads(job.download_data(job.details.output_data_uri)))
        self.data_per_register: Dict[str, Readout] = {k: create_readout(v) for k, v in data.items()}

    def __getitem__(self, register_name: str) -> "Readout":
        return self.data_per_register[register_name]


T = TypeVar("T", bound=Union[int, float, complex])
Readout = List[List[T]]
"""Contains the data of a declared "readout" memory region, usually the ``ro`` register.

All data for all shots for a single Readout will have the same datatype T corresponding to the declared Quil data type:

* ``BIT`` | ``OCTET`` | ``INTEGER``: ``int``
* ``REAL``: ``float``
"""


def create_readout(raw_data: List[List[RawData]]) -> Readout:
    if isinstance(raw_data[0][0], list):
        raw_data = [[complex(entry[0], entry[1]) for entry in shot] for shot in raw_data]

    return raw_data
