##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging

try:
    from .version import __version__
except:
    __version__ = "<unknown>"

logger = logging.getLogger(__name__)
logger.info(f"version: {__version__}")

from .job       import *
from .workspace import *
