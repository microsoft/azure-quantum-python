##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import json

from ... import Job
from ..._client.models import JobDetails
from .result import MicrosoftEstimatorResult

class MicrosoftEstimatorJob(Job):
    """
    A dedicated job class for jobs from the microsoft.estimator target.
    """

    def __init__(self, workspace, job_details: JobDetails, **kwargs):
        super().__init__(workspace, job_details, **kwargs)

    def get_results(self, timeout_secs: float = ...) -> MicrosoftEstimatorResult:
        try:
            results = super().get_results(timeout_secs)
            return MicrosoftEstimatorResult(results)
        except RuntimeError as error:
            error_obj = self.details.error_data
            message = "Cannot retrieve results as job execution failed " \
                      f"({error_obj.code}: {error_obj.message})"
            raise RuntimeError(message)

