##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import io
import json
from typing import Any, Dict

from azure.quantum.aio.target.target import Target
from azure.quantum.aio.job.job import Job
from azure.quantum.aio.workspace import Workspace
from azure.quantum.target import IonQ as SyncIonQ


class IonQ(Target, SyncIonQ):
    """IonQ target."""

    async def submit(
        self,
        circuit: Dict[str, Any],
        name: str = "ionq-job",
        num_shots: int = None,
        input_params: Dict[str, Any] = None,
        **kwargs
    ) -> Job:
        """Submit an IonQ circuit (JSON format)

        :param circuit: Quantum circuit in IonQ JSON format
        :type circuit: Dict[str, Any]
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
            input_params["shots"] = num_shots

        return await super().submit(
            input_data=circuit,
            name=name,
            input_params=input_params,
            **kwargs
        )
