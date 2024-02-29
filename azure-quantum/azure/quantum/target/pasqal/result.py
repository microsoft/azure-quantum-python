"""Defines targets and helper functions for the Pasqal provider"""

##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

__all__ = [
    "Result",
]

import json
from typing import Union, Dict, List, TypeVar, cast

from ...job import Job


class Result:
    """Downloads the data of a completed Job and provides a dictionary of registers.

    .. highlight:: python
    .. code-block::
       from azure.quantum.job import Job
       from azure.quantum.target.pasqal import Result
       job = Job(...)  # This job should come from a Pasqal target
       job.wait_until_completed()
       result = Result(job)

    """

    def __init__(self, job: Job) -> None:
        """
        Decode the results of a Job with output type of "pasqal.pulser-results.v1"

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
        self.data = cast(Dict[str, int], json.loads(job.download_data(job.details.output_data_uri)))

    def __getitem__(self, register_name: str) -> int:
        return self.data[register_name]