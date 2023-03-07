##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
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
        results = super().get_results(timeout_secs)

        return MicrosoftEstimatorResult(results)
