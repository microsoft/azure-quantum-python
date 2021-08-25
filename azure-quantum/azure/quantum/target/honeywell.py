##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import io
from typing import Any, Dict

from azure.quantum.target.target import Target
from azure.quantum.job.job import Job
from azure.quantum.workspace import Workspace


class Honeywell(Target):
    """Honeywell target."""
    target_names = (
        "honeywell.hqs-lt-s1",
        "honeywell.hqs-lt-s1-apival",
        "honeywell.hqs-lt-s1-sim",
    )

    def __init__(
        self,
        workspace: Workspace,
        name: str = "honeywell.hqs-lt-s1-apival",
        input_data_format: str = "honeywell.openqasm.v1",
        output_data_format: str = "honeywell.quantum-results.v1",
        provider_id: str = "honeywell",
        content_type: str = "application/qasm",
        encoding: str = "",
        **kwargs
    ):
        super().__init__(
            workspace=workspace,
            name=name,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            provider_id=provider_id,
            content_type=content_type,
            encoding=encoding,
            **kwargs
        )

    @staticmethod
    def _encode_input_data(data: str) -> bytes:
        stream = io.BytesIO()
        stream.write(data.encode())
        return stream.getvalue()

    def submit(
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

        return super().submit(
            input_data=circuit,
            name=name,
            input_params=input_params,
            **kwargs
        )
