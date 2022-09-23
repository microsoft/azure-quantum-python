##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import Any, Dict

from azure.quantum.aio.job.job import Job
from azure.quantum.aio.target.quantinuum import Quantinuum


class Honeywell(Quantinuum):
    """Quantinuum target."""

    async def submit(
        self,
        circuit: str,
        name: str = "honeywell-job",
        num_shots: int = None,
        input_params: Dict[str, Any] = None,
        **kwargs
    ) -> Job:
        """Submit a Quantinuum program (OpenQASM 2.0 format)

        :param circuit: Quantum circuit in Quantinuum OpenQASM 2.0 format
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
        return await super().submit(
            circuit=circuit,
            name=name,
            num_shots=num_shots,
            input_params=input_params,
            **kwargs
        )
