##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from typing import Any, Dict

from azure.quantum.job.job import Job
from azure.quantum.workspace import Workspace
from azure.quantum.target.honeywell import Honeywell


class Quantinuum(Honeywell):
    """Quantinuum target."""
    target_names = (
        "quantinuum.hqs-lt-s1",
        "quantinuum.hqs-lt-s1-apival",
        "quantinuum.hqs-lt-s1-sim",
    )

    def __init__(
        self,
        workspace: Workspace,
        name: str = "quantinuum.hqs-lt-s1-apival",
        input_data_format: str = "honeywell.openqasm.v1",
        output_data_format: str = "honeywell.quantum-results.v1",
        provider_id: str = "quantinuum",
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

    def submit(
        self,
        circuit: str,
        name: str = "quantinuum-job",
        num_shots: int = None,
        input_params: Dict[str, Any] = None,
        **kwargs
    ) -> Job:
        """Submit a Quantinuum program (QASM format)

        :param circuit: Quantum circuit in Quantinuum QASM format
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
