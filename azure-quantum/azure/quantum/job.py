##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging
import time
import io
import json
import re
import uuid

from typing import List, TYPE_CHECKING
from urllib.parse import urlparse

from msrest.authentication import Authentication
from azure.quantum._client.models import JobDetails
from azure.quantum.storage import download_blob
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobClient, BlobSasPermissions, generate_blob_sas, generate_container_sas

__all__ = ['Job']

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from azure.quantum.workspace import Workspace

class Job:
    """Azure Quantum Job that is submitted to a given Workspace.

    :param workspace: Workspace instance to submit job to
    :type workspace: Workspace
    :param job_details: Job details model, contains Job ID, name and other details
    :type job_details: JobDetails
    """
    def __init__(self, workspace: "Workspace", job_details: JobDetails):
      self.workspace = workspace
      self.details = job_details
      self.id = job_details.id
      self.results = None

    def refresh(self):
        """Refreshes the Job's details by querying the workspace.
        """
        self.details = self.workspace.get_job(self.id).details

    def has_completed(self):
        return (
            self.details.status == "Succeeded" or
            self.details.status == "Failed" or
            self.details.status == "Cancelled"
        )

    def wait_until_completed(self, max_poll_wait_secs=30):
        """Keeps refreshing the Job's details until it reaches a finished status.
        """
        self.refresh()
        poll_wait = 0.2
        while not self.has_completed():
            logger.debug(f"Waiting for job {self.id}, it is in status '{self.details.status}'")
            print('.', end='', flush=True)
            time.sleep(poll_wait)
            self.refresh()
            poll_wait = max_poll_wait_secs if poll_wait >= max_poll_wait_secs else poll_wait * 1.5

    def get_results(self):
        if not self.results is None:
            return self.results

        if not self.has_completed():
            self.wait_until_completed()

        if not self.details.status == "Succeeded":
            raise RuntimeError(f"Cannot retrieve results as job execution failed (status: {self.details.status}. error: {self.details.error_data})")

        url = urlparse(self.details.output_data_uri) 
        if url.query.find('se=') == -1:
            # output_data_uri does not contains SAS token, get sas url from service
            blob_client = BlobClient.from_blob_url(self.details.output_data_uri)
            blob_uri = self.workspace._get_linked_storage_sas_uri(blob_client.container_name, blob_client.blob_name)
            payload = download_blob(blob_uri)
        else:
            # output_data_uri contains SAS token, use it
            payload = download_blob(self.details.output_data_uri)

        result = json.loads(payload.decode('utf8'))
        return result
    
    def get_tags(self) -> List[str]:
        """ Get the existing tags for the job
        """
        if "tags" in self.details.metadata:
            return Job.deserialize_tags(self.details.metadata["tags"])
        else:
            return []

    def update_tags(self, tags: List[str]):
        """ Updates current job metadata with given list of tags. 
            Job must be updated as a submission to the workspace in order for tags to persist.
        """
        if tags and len(tags) > 0:
            self.details.metadata["tags"] = Job.serialize_tags(tags)
            
    @staticmethod
    def create_job_id() -> str:
        """Create a unique id for a new job.
        """
        return str(uuid.uuid1())
    
    @staticmethod
    def serialize_tags(tags: List[str]) -> str:
        """
        Tags are stored in job metadata as comma separated alphanumeric values.
        All special characters (except for _) will be stripped. 
        """
        # \W is a special python character that matches [^a-zA-Z0-9_]
        return ",".join([re.sub(r'\W+', '', tag.lower()) for tag in tags])

    @staticmethod
    def deserialize_tags(tags_string: str) -> List[str]:
        return tags_string.split(',')
