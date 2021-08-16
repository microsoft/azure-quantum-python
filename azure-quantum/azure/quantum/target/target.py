##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import abc
from typing import Any, Dict

from azure.quantum.workspace import Workspace
from azure.quantum.job.job import Job


class Target(abc.ABC):
    """Azure Quantum Target."""
    def __init__(
        self,
        workspace: Workspace,
        name: str,
        input_data_format: str = "",
        output_data_format: str = "",
        provider_id: str = "",
        content_type: str = "",
        encoding: str = ""
    ):
        self.workspace = workspace
        self.name = name
        self.input_data_format = input_data_format
        self.output_data_format = output_data_format
        self.provider_id = provider_id
        self.content_type = content_type
        self.encoding = encoding

    @abc.abstractstaticmethod
    def _encode_input_data(data: Dict[Any, Any]) -> bytes:
        """Implement abstract method to encode input data to bytes

        :param data: Input data
        :type data: Dict[Any, Any]
        :return: Encoded input data
        :rtype: bytes
        """
        pass

    def submit(
        self,
        input_data: Any,
        name: str = "azure-quantum-job",
        input_params: Dict[str, Any] = None,
        **kwargs
    ) -> Job:
        """Submit input data and return Job

        :param input_data: Input data
        :type input_data: Any
        :param name: Job name
        :type name: str
        :param input_params: Input parameters
        :type input_params: Dict[str, Any]
        :return: Azure Quantum job
        :rtype: Job
        """
        input_params = input_params or {}
        blob = self._encode_input_data(data=input_data)

        return Job.from_input_data(
            workspace=self.workspace,
            name=name,
            target=self.name,
            input_data=blob,
            content_type=self.content_type,
            encoding=self.encoding,
            provider_id=self.provider_id,
            input_data_format=self.input_data_format,
            output_data_format=self.output_data_format,
            input_params=input_params,
            **kwargs
        )
