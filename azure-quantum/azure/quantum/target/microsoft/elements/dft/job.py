import collections.abc
import logging
from typing import Any, Dict, Union, Optional
from azure.quantum.job import JobFailedWithResultsError
from azure.quantum.job.base_job import BaseJob, ContentType
from azure.quantum.job.job import Job, DEFAULT_TIMEOUT
from azure.quantum._client.models import JobDetails
from azure.quantum.workspace import Workspace

logger = logging.getLogger(__name__)

class MicrosoftElementsDftJob(Job):
    """
    A dedicated job class for jobs from the microsoft.dft target.
    """

    def __init__(self, workspace, job_details: JobDetails, **kwargs):
        """Azure Quantum Job that is submitted to a given Workspace.

        :param workspace: Workspace instance to submit job to
        :type workspace: Workspace
        :param job_details: Job details model,
                contains Job ID, name and other details
        :type job_details: JobDetails
        """
        super().__init__(workspace, job_details, **kwargs)


    def get_results(self, timeout_secs: float = DEFAULT_TIMEOUT) -> Dict[str, Any]:
        """Get job results by downloading the results blob from the
        storage container linked via the workspace.

        :param timeout_secs: Timeout in seconds, defaults to 300
        :type timeout_secs: float
        :raises: :class:`RuntimeError` if job execution failed.
        :raises: :class:`azure.quantum.job.JobFailedWithResultsError` if job execution failed,
                but failure results could still be retrieved.
        :return: Results dictionary.
        """

        try:
            job_results = super().get_results(timeout_secs)
            return job_results
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

    @classmethod
    def from_input_data_container(
        cls,
        workspace: "Workspace",
        name: str,
        target: str,
        input_data: bytes,
        batch_input_blobs: Dict[str, bytes],
        content_type: ContentType = ContentType.json,
        blob_name: str = "inputData",
        encoding: str = "",
        job_id: str = None,
        container_name: str = None,
        provider_id: str = None,
        input_data_format: str = None,
        output_data_format: str = None,
        input_params: Dict[str, Any] = None,
        session_id: Optional[str] = None,
        **kwargs
    ) -> "BaseJob":
        """Create a new Azure Quantum job based on a list of input_data.

        :param workspace: Azure Quantum workspace to submit the input_data to
        :type workspace: Workspace
        :param name: Name of the job
        :type name: str
        :param target: Azure Quantum target
        :type target: str
        :param input_data: Raw input data to submit
        :type input_data: Dict
        :param blob_name: Dict of Input data json to gives a table of contents
        :type batch_input_blobs: Dict
        :param blob_name: Dict of QcSchema Data where the key is the blob name to store it in the container
        :type blob_name: str
        :param content_type: Content type, e.g. "application/json"
        :type content_type: ContentType
        :param encoding: input_data encoding, e.g. "gzip", defaults to empty string
        :type encoding: str
        :param job_id: Job ID, defaults to None
        :type job_id: str
        :param container_name: Container name, defaults to None
        :type container_name: str
        :param provider_id: Provider ID, defaults to None
        :type provider_id: str
        :param input_data_format: Input data format, defaults to None
        :type input_data_format: str
        :param output_data_format: Output data format, defaults to None
        :type output_data_format: str
        :param input_params: Input parameters, defaults to None
        :type input_params: Dict[str, Any]
        :param input_params: Input params for job
        :type input_params: Dict[str, Any]
        :return: Azure Quantum Job
        :rtype: Job
        """
        # Generate job ID if not specified
        if job_id is None:
            job_id = cls.create_job_id()

        # Create container if it does not yet exist
        container_uri = workspace.get_container_uri(
            job_id=job_id,
            container_name=container_name
        )
        logger.debug(f"Container URI: {container_uri}")

        # Upload Input Data
        input_data_uri = cls.upload_input_data(
            container_uri=container_uri,
            input_data=input_data,
            content_type=content_type,
            blob_name=blob_name,
            encoding=encoding,
        )

        # Upload data to container
        for blob_name, input_data_item in batch_input_blobs.items():
            cls.upload_input_data(
                container_uri=container_uri,
                input_data=input_data_item,
                content_type=content_type,
                blob_name=blob_name,
                encoding=encoding,
            )

        # Create and submit job
        return cls.from_storage_uri(
            workspace=workspace,
            job_id=job_id,
            target=target,
            input_data_uri=input_data_uri,
            container_uri=container_uri,
            name=name,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            provider_id=provider_id,
            input_params=input_params,
            session_id=session_id,
            **kwargs
        )