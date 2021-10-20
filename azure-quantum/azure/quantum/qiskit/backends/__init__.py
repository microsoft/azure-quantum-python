##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from azure.quantum.qiskit.backends.ionq import (
    IonQBackend,
    IonQQPUBackend,
    IonQSimulatorBackend
)

from azure.quantum.qiskit.backends.honeywell import (
    HoneywellBackend,
    HoneywellQPUBackend,
    HoneywellAPIValidatorBackend,
    HoneywellSimulatorBackend
)

# Default targets to use when there is no target class
# associated with a given target ID
DEFAULT_TARGETS = {}
