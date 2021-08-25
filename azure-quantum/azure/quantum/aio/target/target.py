##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import abc
from typing import Any, Dict


from azure.quantum.aio.job.job import Job
from azure.quantum.target import Target as SyncTarget
from azure.quantum.aio.workspace import Workspace


class Target(SyncTarget, abc.ABC):
    """Azure Quantum Target."""
    workspace: Workspace

    async def submit(
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

        return await Job.from_input_data(
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

    async def refresh(self):
        """Update the target availability and queue time"""
        targets = await self.workspace._get_target_status(self.name, self.provider_id)
        if len(targets) > 0:
            _, target_status = targets[0]
            self._current_availability = target_status.current_availability
            self._average_queue_time = target_status.average_queue_time
        else:
            raise ValueError(
                f"Cannot refresh the Target status: \
target '{self.name}' of provider '{self.provider_id}' not found."
            )
