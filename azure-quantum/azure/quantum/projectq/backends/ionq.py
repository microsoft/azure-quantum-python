##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import json
from typing import TYPE_CHECKING
from azure.quantum import __version__
from azure.quantum.qiskit.job import AzureQuantumJob

try:
    import projectq
except ImportError:
    raise ImportError(
    "Missing optional 'projectq' dependencies. \
To install run: pip install azure-quantum[projectq]"
)

if TYPE_CHECKING:
    from azure.quantum.projectq import AzureQuantumProvider

import logging
logger = logging.getLogger(__name__)

__all__ = ["IonQBackend", "IonQQPUBackend", "IonQSimulatorBackend"]


class IonQBackend:
    pass


class IonQQPUBackend:
    pass


class IonQSimulatorBackend:
    pass
