##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import io
import gzip
from typing import Any, Dict

from azure.quantum.target.target import Target
from azure.quantum.job.job import Job
from azure.quantum.workspace import Workspace


class FleetManagement(Target):
    """Microsoft Fleet Management target."""

    def __init__(
        self,
        workspace: Workspace,
        name: str = "microsoft.fleetmanagement",
        input_data_format: str = "microsoft.fleetmanagement.v1",
        output_data_format: str = "microsoft.fleetmanagement-results.v1",
        provider_id: str = "Microsoft.FleetManagement",
        content_type: str = "application/json",
        encoding: str = "gzip"
    ):
        super().__init__(
            workspace=workspace,
            name=name,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            provider_id=provider_id,
            content_type=content_type,
            encoding=encoding
        )

    @staticmethod
    def _encode_input_data(data: str) -> bytes:
        stream = io.BytesIO()
        with gzip.GzipFile(fileobj=stream, mode="w") as fo:
            fo.write(data.encode())
        return stream.getvalue()

    def submit(
        self,
        input: str,
        name: str = "fleet-management-job",
        input_params: Dict[str, Any] = None,
        **kwargs
    ) -> Job:
        """Submit a Fleet Management problem

        :param input: Input in json format
        :type input: str
        :param name: Job name
        :type name: str
        :param input_params: Optional input params dict
        :type input_params: Dict[str, Any]
        :return: Azure Quantum job
        :rtype: Job
        """
        if input_params is None:
            input_params = {}

        return super().submit(
            input_data=input,
            name=name,
            input_params=input_params,
            **kwargs
        )
