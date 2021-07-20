##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging
from azure.quantum.version import __version__

from .job import *
from .workspace import *
from .storage import *

logger = logging.getLogger(__name__)
logger.info(f"version: {__version__}")
