##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##


import logging
import time
import json

from typing import TYPE_CHECKING

from azure.quantum._client.models import JobDetails
from azure.quantum.job.job_failed_with_results_error import JobFailedWithResultsError
from azure.quantum.job.base_job import BaseJob, ContentType, DEFAULT_TIMEOUT
from azure.quantum.job.filtered_job import FilteredJob

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

    _default_poll_wait = 0.2

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
        :type max_poll_wait_secs: int
        :param timeout_secs: Timeout in seconds, defaults to None
        :type timeout_secs: int
        :param print_progress: Print "." to stdout to display progress
        :type print_progress: bool
        :raises: :class:`TimeoutError` If the total poll time exceeds timeout, raise.
        """
        self.refresh()
        poll_wait = Job._default_poll_wait
        start_time = time.time()
        while not self.has_completed():
            if timeout_secs is not None and (time.time() - start_time) >= timeout_secs:
                raise TimeoutError(f"The wait time has exceeded {timeout_secs} seconds.")

            logger.debug(
                f"Waiting for job {self.id},"
                + f"it is in status '{self.details.status}'"
            )
            if print_progress:
                print(".", end="", flush=True)
            time.sleep(poll_wait)
            self.refresh()
            poll_wait = (
                max_poll_wait_secs
                if poll_wait >= max_poll_wait_secs
                else poll_wait * 1.5
            )

    def get_results(self, timeout_secs: float = DEFAULT_TIMEOUT):
        """Get job results by downloading the results blob from the
        storage container linked via the workspace.

        Raises :class:`RuntimeError` if job execution fails.

        :param timeout_secs: Timeout in seconds, defaults to 300
        :type timeout_secs: float
        :return: Results dictionary with histogram shots, or raw results if not a json object.
        :rtype: Any
        """
        if self.results is not None:
            return self.results

        if not self.has_completed():
            self.wait_until_completed(timeout_secs=timeout_secs)

        if not self.details.status == "Succeeded":
            if self.details.status == "Failed" and self._allow_failure_results():
                job_blob_properties = self.download_blob_properties(self.details.output_data_uri)
                if job_blob_properties.size > 0:
                    job_failure_data = self.download_data(self.details.output_data_uri)
                    raise JobFailedWithResultsError("An error occurred during job execution.", job_failure_data)

            raise RuntimeError(
                f'{"Cannot retrieve results as job execution failed"}'
                + f"(status: {self.details.status}."
                + f"error: {self.details.error_data})"
            )

        payload = self.download_data(self.details.output_data_uri)
        try:
            payload = payload.decode("utf8")
            results = json.loads(payload)

            if self.details.output_data_format == "microsoft.quantum-results.v1":
                if "Histogram" not in results:
                    raise f"\"Histogram\" array was expected to be in the Job results for \"{self.details.output_data_format}\" output format."
                
                histogram_values = results["Histogram"]

                if len(histogram_values) % 2 == 0:
                    # Re-mapping {'Histogram': ['[0]', 0.50, '[1]', 0.50] } to {'[0]': 0.50, '[1]': 0.50}
                    return {histogram_values[i]: histogram_values[i + 1] for i in range(0, len(histogram_values), 2)}
                else: 
                    raise f"\"Histogram\" array has invalid format. Even number of items is expected."
            
            return results
        except:
            # If errors decoding the data, return the raw payload:
            return payload


    @classmethod
    def _allow_failure_results(cls) -> bool: 
        """
        Allow to download job results even if the Job status is "Failed".

        This method can be overridden in derived classes to alter the default
        behaviour.

        The default is False.
        """
        return False