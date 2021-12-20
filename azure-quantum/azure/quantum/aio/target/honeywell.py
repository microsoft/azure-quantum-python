##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import Any, Dict

from azure.quantum.aio.target.target import Target
from azure.quantum.aio.job.job import Job
from azure.quantum.target import Honeywell as SyncHoneywell


class Honeywell(Target, SyncHoneywell):
    """Honeywell target."""

    async def submit(
        self,
        circuit: str,
        name: str = "honeywell-job",
        num_shots: int = None,
        input_params: Dict[str, Any] = None,
        **kwargs
    ) -> Job:
        """Submit a Honeywell program (QASM format)

        :param circuit: Quantum circuit in Honeywell QASM format
        :type circuit: str
        :param name: Job name
        :type name: str
        :param num_shots: Number of shots, defaults to None
        :type num_shots: int
        :param input_params: Optional input params dict
        :type input_params: Dict[str, Any]
        :return: Azure Quantum job
        :rtype: Job
        """
        if input_params is None:
            input_params = {}
        if num_shots is not None:
            input_params = input_params.copy()
            input_params["count"] = num_shots

        return await super().submit(
            input_data=circuit,
            name=name,
            input_params=input_params,
            **kwargs
        )
