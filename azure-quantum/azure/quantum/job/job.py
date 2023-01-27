##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging
import time
import json

from typing import TYPE_CHECKING

from azure.quantum._client.models import JobDetails
from azure.quantum.job.base_job import BaseJob, ContentType, DEFAULT_TIMEOUT
from azure.quantum.job.filtered_job import FilteredJob
from azure.quantum.job.workspace_item import WorkspaceItem
from azure.quantum._client.models import JobDetails

__all__ = ["Job", "JobDetails"]

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

    def __init__(self, workspace: "Workspace", job_details: JobDetails, **kwargs):
        self.results = None
        super().__init__(
            workspace=workspace,
            details=job_details,
            **kwargs
        )
    
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

    def wait_until_completed(
        self,
        max_poll_wait_secs=30,
        timeout_secs=None,
        print_progress=True
    ) -> None:
        """Keeps refreshing the Job's details
        until it reaches a finished status.

        :param max_poll_wait_secs: Maximum poll wait time, defaults to 30
        :type max_poll_wait_secs: int, optional
        :param timeout_secs: Timeout in seconds, defaults to None
        :type timeout_secs: int, optional
        :param print_progress: Print "." to stdout to display progress
        :type print_progress: bool, optional
        :raises TimeoutError: If the total poll time exceeds timeout, raise
        """
        self.refresh()
        poll_wait = 0.2
        total_time = 0.
        while not self.has_completed():
            if timeout_secs is not None and total_time >= timeout_secs:
                raise TimeoutError(f"The wait time has exceeded {timeout_secs} seconds.")
 
            logger.debug(
                f"Waiting for job {self.id},"
                + f"it is in status '{self.details.status}'"
            )
            if print_progress:
                print(".", end="", flush=True)
            time.sleep(poll_wait)
            total_time += poll_wait
            self.refresh()
            poll_wait = (
                max_poll_wait_secs
                if poll_wait >= max_poll_wait_secs
                else poll_wait * 1.5
            )

    def get_results(self, timeout_secs: float = DEFAULT_TIMEOUT):
        """Get job results by downloading the results blob from the
        storage container linked via the workspace.

        :param timeout_secs: Timeout in seconds, defaults to 300
        :type timeout_secs: int
        :raises RuntimeError: Raises RuntimeError if job execution failed
        :return: Results dictionary with histogram shots, or raw results if not a json object.
        """
        if self.results is not None:
            return self.results

        if not self.has_completed():
            self.wait_until_completed(timeout_secs=timeout_secs)

        if not self.details.status == "Succeeded":
            raise RuntimeError(
                f'{"Cannot retrieve results as job execution failed"}'
                + f"(status: {self.details.status}."
                + f"error: {self.details.error_data})"
            )

        payload = self.download_data(self.details.output_data_uri)
        try:
            payload = payload.decode("utf8")
            return json.loads(payload)
        except:
            # If errors decoding the data, return the raw payload:
            return payload
