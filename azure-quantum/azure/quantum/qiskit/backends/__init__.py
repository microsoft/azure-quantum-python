##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from azure.quantum.qiskit.backends.ionq import (
    IonQBackend,
    IonQQPUBackend,
    IonQAriaBackend,
    IonQSimulatorBackend,
    IonQQPUQirBackend,
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

from azure.quantum.qiskit.backends.microsoft import (
    MicrosoftBackend,
    MicrosoftResourceEstimationBackend,
)
