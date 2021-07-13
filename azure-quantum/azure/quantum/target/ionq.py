##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import io
import json
from typing import Any, Dict

from azure.quantum.target.target import Target
from azure.quantum.job.job import Job
from azure.quantum.workspace import Workspace


class IonQ(Target):
    """IonQ target."""

    def __init__(
        self,
        workspace: Workspace,
        target: str = "ionq.simulator",
        input_data_format: str = "ionq.circuit.v1",
        output_data_format: str = "ionq.quantum-results.v1",
        provider_id: str = "IonQ",
        content_type: str = "application/json",
        encoding: str = ""
    ):
        super().__init__(
            workspace=workspace,
            target=target,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            provider_id=provider_id,
            content_type=content_type,
            encoding=encoding
        )

    @staticmethod
    def _encode_input_data(data: Dict[Any, Any]) -> bytes:
        buffer = io.BytesIO()
        data = json.dumps(data)
        buffer.write(data.encode())
        return buffer.getvalue()

    def submit(
        self,
        circuit: Dict[str, Any],
        name: str = None
    ) -> Job:
        """Submit an IonQ circuit (JSON format)

        :param circuit: Quantum circuit in IonQ JSON format
        :type circuit: Dict[str, Any]
        :param name: Job name
        :type name: str
        :return: Azure Quantum job
        :rtype: Job
        """
        blob = self._encode_input_data(circuit)
        return self.submit_input_data(input_data=blob, name=name)
