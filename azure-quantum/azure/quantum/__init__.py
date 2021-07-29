##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import os
import logging
from .version import __version__

from .job.job import *
from .workspace import *

logger = logging.getLogger(__name__)
logger.info(f"version: {__version__}")

# Add plugins to azure.quantum namespace
__path__ += [os.path.join(__path__[0], "plugins/")]
