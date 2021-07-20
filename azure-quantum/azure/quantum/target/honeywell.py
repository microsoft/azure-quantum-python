##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import io

from azure.quantum.target.target import Target
from azure.quantum.job.job import Job
from azure.quantum.workspace import Workspace


class Honeywell(Target):
    """Honeywell target."""

    def __init__(
        self,
        workspace: Workspace,
        target: str = "",
        input_data_format: str = "honeywell.openqasm.v1",
        output_data_format: str = "honeywell.quantum-results.v1",
        provider_id: str = "honeywell",
        content_type: str = "application/qasm",
        encoding: str = "honeywell.hqs-lt-s1-apival"
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
    def _encode_input_data(data: str) -> bytes:
        stream = io.BytesIO()
        stream.write(data.encode())
        return stream.getvalue()

    def submit(
        self,
        circuit: str,
        name: str = None
    ) -> Job:
        """Submit a Honeywell program (QASM format)

        :param circuit: Quantum circuit in Honeywell QASM format
        :type circuit: str
        :param name: Job name
        :type name: str
        :return: Azure Quantum job
        :rtype: Job
        """
        blob = self._encode_input_data(circuit)
        return self._submit_encoded_input_data(input_data=blob, name=name)
