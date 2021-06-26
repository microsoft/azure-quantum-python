##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import io
import json
from typing import Any, Dict

from azure.quantum.providers.provider_job import ProviderJobMixin
from azure.quantum.workspace import Workspace
from azure.quantum.job import DEFAULT_TIMEOUT, Job

_IonQJson = Dict[str, Any]


class IonqJob(ProviderJobMixin, Job):
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
        timeout: int = DEFAULT_TIMEOUT
    ) -> IonqJob:
        """Submit blob data to the service

        :param blob: Blob data to submit to Azure Quantum
        :type blob: bytes
        :param name: Blob name
        :type name: str
        :param timeout: Job submission timeout, defaults to DEFAULT_TIMEOUT
        :type timeout: int, optional
        :return: [description]
        :rtype: IonQJob
        """
        job = IonqJob.from_blob(
            workspace=self.workspace,
            target=self.target,
            blob=blob,
            name=name,
            timeout=timeout
        )
        job.submit()
        return job

    def submit(
        self,
        circuit: _IonQJson,
        name: str = None,
        timeout: int = DEFAULT_TIMEOUT
    ) -> ProviderJobMixin:
        """Submit an IonQ circuit (JSON format)

        :param circuit: Quantum circuit in IonQ JSON format
        :type circuit: Dict[str, Any]
        :return: Azure Quantum job
        :rtype: Job
        """
        blob = self._encode_json_data(circuit)
        self.submit_blob(blob=blob, name=name, timeout=timeout)
