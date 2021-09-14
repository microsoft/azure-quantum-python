##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import abc
from typing import Any, Dict

from azure.quantum._client.models import TargetStatus
from azure.quantum.workspace import Workspace
from azure.quantum.job.job import Job


class Target(abc.ABC):
    """Azure Quantum Target."""
    # Target IDs that are compatible with this Target class.
    target_names = ()
    provider_id = ""
    def __init__(
        self,
        workspace: Workspace,
        name: str,
        input_data_format: str = "",
        output_data_format: str = "",
        provider_id: str = "",
        content_type: str = "",
        encoding: str = "",
        average_queue_time: float = None,
        current_availability: str = ""
    ):
        self.workspace = workspace
        self.name = name
        self.input_data_format = input_data_format
        self.output_data_format = output_data_format
        self.provider_id = provider_id
        self.content_type = content_type
        self.encoding = encoding
        self._average_queue_time = average_queue_time
        self._current_availability = current_availability

    def __repr__(self):
        return f"<Target name=\"{self.name}\", \
avg. queue time={self._average_queue_time} s, {self._current_availability}>"

    @classmethod
    def from_target_status(
        cls, workspace: Workspace, status: TargetStatus, **kwargs
    ):
        """Create a Target instance from a given workspace and target status.

        :param workspace: Associated workspace
        :type workspace: Workspace
        :param status: Target status with availability and current queue time
        :type status: TargetStatus
        :return: Target instance
        :rtype: Target
        """
        return cls(
            workspace=workspace,
            name=status.id,
            average_queue_time=status.average_queue_time,
            current_availability=status.current_availability,
            **kwargs
        )
    
    def refresh(self):
        """Update the target availability and queue time"""
        targets = self.workspace._get_target_status(self.name, self.provider_id)
        if len(targets) > 0:
            _, target_status = targets[0]
            self._current_availability = target_status.current_availability
            self._average_queue_time = target_status.average_queue_time
        else:
            raise ValueError(
                f"Cannot refresh the Target status: \
target '{self.name}' of provider '{self.provider_id}' not found."
            )

    @property
    def current_availability(self):
        return self._current_availability
    
    @property
    def average_queue_time(self):
        return self._average_queue_time

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
