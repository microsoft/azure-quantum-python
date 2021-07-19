##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from datetime import datetime
import logging

from typing import List, Optional

from azure.quantum._client.aio import QuantumClient
from azure.quantum._client.aio.operations import JobsOperations, StorageOperations
from azure.quantum._client.models import JobStatus
from azure.quantum import AsyncJob

from azure.quantum.workspace import Workspace, BASE_URL

from .version import __version__

logger = logging.getLogger(__name__)

__all__ = ["AsyncWorkspace"]


class AsyncWorkspace(Workspace):

    credentials = None

    def _create_client(self) -> QuantumClient:
        base_url = BASE_URL(self.location)
        logger.debug(
            f"Creating client for: subs:{self.subscription_id},"
            + f"rg={self.resource_group}, ws={self.name}, frontdoor={base_url}"
        )

        client = QuantumClient(
            credential=self.credentials,
            subscription_id=self.subscription_id,
            resource_group_name=self.resource_group,
            workspace_name=self.name,
            base_url=base_url,
        )
        return client

    def _create_jobs_client(self) -> JobsOperations:
        client = self._create_client().jobs
        return client

    def _create_workspace_storage_client(self) -> StorageOperations:
        client = self._create_client().storage
        return client

    async def submit_job(self, job: AsyncJob) -> AsyncJob:
        client = self._create_jobs_client()
        details = await client.create(
            job.details.id, job.details
        )
        return AsyncJob(self, details)

    async def cancel_job(self, job: AsyncJob) -> AsyncJob:
        client = self._create_jobs_client()
        await client.cancel(job.details.id)
        details = await client.get(job.id)
        return AsyncJob(self, details)

    async def get_job(self, job_id: str) -> AsyncJob:
        """Returns the job corresponding to the given id."""
        client = self._create_jobs_client()
        details = await client.get(job_id)
        return AsyncJob(self, details)

    async def list_jobs(
        self, 
        name_match: str = None, 
        status: Optional[JobStatus] = None,
        created_after: Optional[datetime] = None
    ) -> List[AsyncJob]:
        """Returns list of jobs that meet optional (limited) filter criteria. 
            :param name_match: regex expression for job name matching
            :param status: filter by job status
            :param created_after: filter jobs after time of job creation
        """
        client = self._create_jobs_client()
        jobs = client.list()

        result = []
        async for j in jobs:
            deserialized_job = AsyncJob(self, j)
            if deserialized_job.matches_filter(name_match, status, created_after):
                result.append(deserialized_job)

        return result
