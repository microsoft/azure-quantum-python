from ... import Job
from ..._client.models import JobDetails

class MicrosoftEstimatorJob(Job):
    """
    A dedicated job class for jobs from the microsoft.estimator target.
    """

    def __init__(self, workspace, job_details: JobDetails, **kwargs):
        super().__init__(workspace, job_details, **kwargs)
