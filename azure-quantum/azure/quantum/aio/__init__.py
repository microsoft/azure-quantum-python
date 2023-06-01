##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging
from azure.quantum.version import __version__

from .job.job import *
from .workspace import *

from azure.quantum._client.models._enums import JobStatus

logger = logging.getLogger(__name__)
logger.info(f"version: {__version__}")
