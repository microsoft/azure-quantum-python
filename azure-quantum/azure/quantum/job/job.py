##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging
import time
import json

from typing import TYPE_CHECKING

from azure.quantum._client.models import JobDetails
from azure.quantum.job.base_job import BaseJob
from azure.quantum.job.filtered_job import FilteredJob

__all__ = ["Job"]

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from azure.quantum.workspace import Workspace


_log = logging.getLogger(__name__)

class Job(BaseJob, FilteredJob):
    """Azure Quantum Job that is submitted to a given Workspace.

    :param workspace: Workspace instance to submit job to
    :type workspace: Workspace
    :param job_details: Job details model,
            contains Job ID, name and other details
    :type job_details: JobDetails
    """

    def __init__(self, workspace: "Workspace", job_details: JobDetails):
        self.workspace = workspace
        self.details = job_details
        self.id = job_details.id
        self.results = None
    
    def submit(self):
        """Submit a job to Azure Quantum."""
        _log.debug(f"Submitting job with ID {self.id}")
        job = self.workspace.submit_job(self)
        self.details = job.details

    def refresh(self):
        """Refreshes the Job's details by querying the workspace."""
        self.details = self.workspace.get_job(self.id).details

    def has_completed(self) -> bool:
        """Check if the job has completed."""
        return (
            self.details.status == "Succeeded"
            or self.details.status == "Failed"
            or self.details.status == "Cancelled"
        )

    def wait_until_completed(self, max_poll_wait_secs=30) -> None:
        """Keeps refreshing the Job's details
        until it reaches a finished status."""
        self.refresh()
        poll_wait = 0.2
        while not self.has_completed():
            logger.debug(
                f"Waiting for job {self.id},"
                + f"it is in status '{self.details.status}'"
            )
            print(".", end="", flush=True)
            time.sleep(poll_wait)
            self.refresh()
            poll_wait = (
                max_poll_wait_secs
                if poll_wait >= max_poll_wait_secs
                else poll_wait * 1.5
            )

    def get_results(self) -> dict:
        """Get job results by downloading the results blob from the
        storage container linked via the workspace.

        :raises RuntimeError: [description]
        :return: [description]
        :rtype: dict
        """
        if self.results is not None:
            return self.results

        if not self.has_completed():
            self.wait_until_completed()

        if not self.details.status == "Succeeded":
            raise RuntimeError(
                f'{"Cannot retrieve results as job execution failed"}'
                + f"(status: {self.details.status}."
                + f"error: {self.details.error_data})"
            )

        payload = self.download_data(self.details.output_data_uri)
        results = json.loads(payload.decode("utf8"))
        return results
