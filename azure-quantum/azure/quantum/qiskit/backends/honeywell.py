##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from typing import TYPE_CHECKING, Union, List
from azure.quantum.version import __version__
from azure.quantum.qiskit.backends.quantinuum import (
    QuantinuumBackend,
    QuantinuumAPIValidatorBackend,
    QuantinuumSimulatorBackend,
    QuantinuumQPUBackend,
    HONEYWELL_PROVIDER_ID
    )

try:
    from qiskit import QuantumCircuit

except ImportError:
    raise ImportError(
    "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
)

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

__all__ = [
    "HoneywellBackend",
    "HoneywellQPUBackend",
    "HoneywellAPIValidatorBackend",
    "HoneywellSimulatorBackend"
]


class HoneywellBackend(QuantinuumBackend):
    """Base class for interfacing with a Quantinuum (formerly Honeywell) backend in Azure Quantum"""

    def __init__(
        self,
        **kwargs
    ):
        super().__init__(provider_id=HONEYWELL_PROVIDER_ID,
                         **kwargs)

    def run(self,
            circuit: Union[QuantumCircuit, List[QuantumCircuit]],
            **kwargs):
        """Submits the given circuit for execution on a Honeywell target."""
        return super().run(circuit, **kwargs)


class HoneywellAPIValidatorBackend(QuantinuumAPIValidatorBackend):
    backend_names = (
        "honeywell.hqs-lt-s1-apival",
        "honeywell.hqs-lt-s2-apival"
    )

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        super().__init__(name=name,
                         provider=provider,
                         provider_id=HONEYWELL_PROVIDER_ID,
                         **kwargs)


class HoneywellSimulatorBackend(QuantinuumSimulatorBackend):
    backend_names = (
        "honeywell.hqs-lt-s1-sim",
        "honeywell.hqs-lt-s2-sim"
    )

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        super().__init__(name=name,
                         provider=provider,
                         provider_id=HONEYWELL_PROVIDER_ID,
                         **kwargs)


class HoneywellQPUBackend(QuantinuumQPUBackend):
    backend_names = (
        "honeywell.hqs-lt-s1",
        "honeywell.hqs-lt-s2"
    )

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        super().__init__(name=name,
                         provider=provider,
                         provider_id=HONEYWELL_PROVIDER_ID,
                         **kwargs)
