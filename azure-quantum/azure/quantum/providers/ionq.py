##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import io
import json
from typing import Any, Dict

from azure.quantum.workspace import Workspace
from azure.quantum.job import Job

_IonQJson = Dict[str, Any]


class IonqJob(Job):
    input_data_format = "ionq.circuit.v1"
    output_data_format = "ionq.quantum-results.v1"
    provider_id = "IonQ"


class IonQ:
    def __init__(
        self,
        workspace: Workspace,
        target: str = "ionq.simulator"
    ):
        self.workspace = workspace
        self.target = target

    @staticmethod
    def _encode_json_data(data: Dict[Any, Any]) -> bytes:
        data = io.BytesIO()
        data = json.dumps(data)
        data.write(data.encode())
        return data.getvalue()

    def submit_blob(
        self,
        blob: bytes,
        name: str,
        blob_name: str = "inputData"
    ) -> IonqJob:
        """Submit blob data to the service

        :param blob: Blob data to submit to Azure Quantum
        :type blob: bytes
        :param name: Job name
        :type name: str
        :param blob_name: Blob name
        :type blob_name: str
        :return: IonqJob instance
        :rtype: IonqJob
        """
        job = IonqJob.from_blob(
            workspace=self.workspace,
            name=name,
            target=self.target,
            blob=blob,
            blob_name=blob_name
        )
        job.submit()
        return job

    def submit(
        self,
        circuit: _IonQJson,
        name: str = None
    ) -> IonqJob:
        """Submit an IonQ circuit (JSON format)

        :param circuit: Quantum circuit in IonQ JSON format
        :type circuit: Dict[str, Any]
        :param name: Job name
        :type name: str
        :return: Azure Quantum job
        :rtype: Job
        """
        blob = self._encode_json_data(circuit)
        return self.submit_blob(blob=blob, name=name)
