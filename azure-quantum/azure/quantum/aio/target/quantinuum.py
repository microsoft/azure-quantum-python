##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from typing import Any, Dict

from azure.quantum.aio.target.target import Target
from azure.quantum.aio.job.job import Job
from azure.quantum.aio.target import Honeywell


class Quantinuum(Honeywell):
    """Quantinuum target."""

    async def submit(
        self,
        circuit: str,
        name: str = "quantinuum-job",
        num_shots: int = None,
        input_params: Dict[str, Any] = None,
        **kwargs
    ) -> Job:
        """Submit a Quantinuum program (QASM format)

        :param circuit: Quantum circuit in Quantinuum (formerly Honeywell) QASM format
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
