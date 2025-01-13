##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

"""Defines set of backends for interacting with Azure Quantum"""

from azure.quantum.qiskit.backends.ionq import (
    IonQBackend,
    IonQAriaBackend,
    IonQSimulatorBackend,
    IonQAriaQirBackend,
    IonQForteBackend,
    IonQForteQirBackend,
    IonQSimulatorQirBackend,
)

from azure.quantum.qiskit.backends.quantinuum import (
    QuantinuumBackend,
    QuantinuumQPUBackend,
    QuantinuumSyntaxCheckerBackend,
    QuantinuumEmulatorBackend,
    QuantinuumQPUQirBackend,
    QuantinuumSyntaxCheckerQirBackend,
    QuantinuumEmulatorQirBackend,
)

from azure.quantum.qiskit.backends.rigetti import (
    RigettiBackend,
    RigettiQPUBackend,
    RigettiSimulatorBackend,
)

from azure.quantum.qiskit.backends.qci import (
    QCIBackend,
    QCISimulatorBackend,
    QCIQPUBackend,
)

# from azure.quantum.qiskit.backends.microsoft import (
#     MicrosoftBackend,
#     MicrosoftResourceEstimationBackend,
# )

from .backend import AzureBackendBase

__all__ = [
    "AzureBackendBase"
]