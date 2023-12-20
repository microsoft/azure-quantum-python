import json
from typing import Any, Dict
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
        except RuntimeError as e:
            if self.details.status == "Failed":
                job_blob_properties = self.download_blob_properties(self.details.output_data_uri)
                if job_blob_properties.size > 0:
                    job_failure_data = self.download_data(self.details.output_data_uri)
                    raise DftRuntimeError("An error occurred during DFT-job execution. " \
                                          "Use error.get_details() for more information.", job_failure_data) from e
            raise


class DftRuntimeError(RuntimeError):

    def __init__(self, message: str, details: Any, *args: object) -> None:
        self._set_error_details(message, details)
        super().__init__(message, *args)

    def _set_error_details(self, message: str, details: Any):
        try:
            details = details.decode("utf8")
            self._details: Dict[str, Any] = json.loads(details)
            if "results" in self._details \
                    and len(self._details["results"]) > 0 \
                    and "error" in self._details["results"][0] \
                    and "error_message" in self._details["results"][0]["error"]:
                self._message = f'{message} Inner error: {self._details["results"][0]["error"]["error_message"]}' 
        except:
            self._details = details
            self._message = message


    def get_details(self) -> Any:
        """
        Get error details.
        """
        return self._details
    

    def __str__(self):
        return f"{self._message}\nDetails: {self._details}"