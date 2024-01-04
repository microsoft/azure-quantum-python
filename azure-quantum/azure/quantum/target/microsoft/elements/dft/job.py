import collections.abc
from typing import Any, Dict, Union
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
                if MicrosoftElementsDftJob._is_dft_failure_results(failure_results):
                    error = failure_results["results"][0]["error"]
                    message = f'{e.get_message()} Error type: {error["error_type"]}. Message: {error["error_message"]}'
                    raise JobFailedWithResultsError(message, failure_results) from None


    @classmethod
    def _allow_failure_results(cls) -> bool: 
        """
        Allow to download job results even if the Job status is "Failed".
        """
        return True


    @staticmethod
    def _is_dft_failure_results(failure_results: Union[Dict[str, Any], str]) -> bool:
         return isinstance(failure_results, dict) \
                    and "results" in failure_results \
                    and isinstance(failure_results["results"], collections.abc.Sequence) \
                    and len(failure_results["results"]) > 0 \
                    and isinstance(failure_results["results"][0], dict) \
                    and "error" in failure_results["results"][0] \
                    and isinstance(failure_results["results"][0]["error"], dict) \
                    and "error_type" in failure_results["results"][0]["error"] \
                    and "error_message" in failure_results["results"][0]["error"]