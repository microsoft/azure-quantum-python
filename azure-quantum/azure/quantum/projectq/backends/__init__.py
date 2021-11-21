##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from azure.quantum.projectq.backends.ionq import (
    IonQBackend,
    IonQQPUBackend,
    IonQSimulatorBackend
)

# Default targets to use when there is no target class
# associated with a given target ID
DEFAULT_TARGETS = {}
