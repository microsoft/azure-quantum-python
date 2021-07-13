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
        target: str,
        input_data_format: str = "",
        output_data_format: str = "",
        provider_id: str = "",
        content_type: str = "",
        encoding: str = ""
    ):
        self.workspace = workspace
        self.target = target
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

    def submit_input_data(
        self,
        input_data: bytes,
        name: str,
        blob_name: str = "inputData"
    ) -> Job:
        """Submit blob data to the Azure Quantum service

        :param blob: Blob data to submit to Azure Quantum
        :type blob: bytes
        :param name: Job name
        :type name: str
        :param blob_name: Blob name
        :type blob_name: str
        :return: Job instance
        :rtype: Job
        """
        job = Job.from_input_data(
            workspace=self.workspace,
            name=name,
            target=self.target,
            input_data=input_data,
            blob_name=blob_name,
            content_type=self.content_type,
            encoding=self.encoding,
            provider_id=self.provider_id,
            input_data_format=self.input_data_format,
            output_data_format=self.output_data_format
        )
        job.submit()
        return job

    def submit(
        self,
        input_data: Any,
        name: str = None
    ) -> Job:
        """Submit input data and return Job

        :param input_data: Input data
        :type input_data: Any
        :param name: Job name
        :type name: str
        :return: Azure Quantum job
        :rtype: Job
        """
        blob = self._encode_input_data(data=input_data)
        return self.submit_input_data(blob=blob, name=name)
