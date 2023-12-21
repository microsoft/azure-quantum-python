from typing import Any, Dict
from azure.quantum.job import JobFailedWithResultsError
from azure.quantum.job.job import Job, DEFAULT_TIMEOUT
from azure.quantum._client.models import JobDetails

class MicrosoftElementsDftJob(Job):
    """
    A dedicated job class for jobs from the microsoft.dft target.
    """

    def __init__(self, workspace, job_details: JobDetails, **kwargs):
        super().__init__(workspace, job_details, **kwargs)


    def get_results(self, timeout_secs: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
        try:
            job_results = super().get_results(timeout_secs)
            return job_results["results"]
        except JobFailedWithResultsError as e:
                failure_results = e.get_failure_results()
                if "results" in failure_results \
                    and len(failure_results["results"]) > 0 \
                    and "error" in failure_results["results"][0] \
                    and "error_message" in failure_results["results"][0]["error"]:
                    message = f'{e.get_message()} Inner error: {failure_results["results"][0]["error"]["error_message"]}'
                    raise JobFailedWithResultsError(message, failure_results) from None


    @classmethod
    def _allow_failure_results(self) -> bool: 
        """
        Allow to download job results even if the Job status is "Failed".
        """
        return True