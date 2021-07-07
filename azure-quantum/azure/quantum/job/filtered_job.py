##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import re
import abc

from typing import Optional
from datetime import datetime, timezone

from azure.quantum._client.models import JobStatus


class FilteredJob(abc.ABC):
    """
    Mixin for adding methods to filter jobs
    """
    def matches_filter(
        self, 
        name_match: str = None, 
        status:  Optional[JobStatus] = None,
        created_after: Optional[datetime] = None
    ) -> bool:
        """Checks if job (self) matches the given properties if any.
            :param name_match: regex expression for job name matching
            :param status: filter by job status
            :param created_after: filter jobs after time of job creation
        """
        if name_match is not None and re.search(name_match, self.details.name) is None:
           return False
        
        if status is not None and self.details.status != status.value:
            return False
        
        if created_after is not None and self.details.creation_time.replace(tzinfo=timezone.utc) < created_after.replace(tzinfo=timezone.utc):
            return False

        return True
