##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from typing import TYPE_CHECKING, Union, List
from azure.quantum.version import __version__
from azure.quantum.qiskit.backends.honeywell import (
    HoneywellBackend,
    HoneywellAPIValidatorBackend,
    HoneywellSimulatorBackend,
    HoneywellQPUBackend)

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
    "QuantinuumBackend",
    "QuantinuumQPUBackend",
    "QuantinuumAPIValidatorBackend",
    "QuantinuumSimulatorBackend"
]

QUANTINUUM_PROVIDER_ID = "quantinuum"

class QuantinuumBackend(HoneywellBackend):
    """Base class for interfacing with a Quantinuum backend in Azure Quantum"""

    def __init__(
        self,
        **kwargs
    ):
        super().__init__(provider_id=QUANTINUUM_PROVIDER_ID,
                         **kwargs)

    def run(self,
            circuit: Union[QuantumCircuit, List[QuantumCircuit]],
            **kwargs):
        """Submits the given circuit for execution on a Quantinuum target."""
        return super().run(circuit, **kwargs)


class QuantinuumAPIValidatorBackend(HoneywellAPIValidatorBackend):
    backend_names = (
        "quantinuum.hqs-lt-s1-apival",
        "quantinuum.hqs-lt-s2-apival"
    )

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        super().__init__(name=name,
                         provider=provider,
                         provider_id=QUANTINUUM_PROVIDER_ID,
                         **kwargs)


class QuantinuumSimulatorBackend(HoneywellSimulatorBackend):
    backend_names = (
        "quantinuum.hqs-lt-s1-sim",
        "quantinuum.hqs-lt-s2-sim"
    )

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        super().__init__(name=name,
                         provider=provider,
                         provider_id=QUANTINUUM_PROVIDER_ID,
                         **kwargs)


class QuantinuumQPUBackend(HoneywellQPUBackend):
    backend_names = (
        "quantinuum.hqs-lt-s1",
        "quantinuum.hqs-lt-s2"
    )

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        super().__init__(name=name,
                         provider=provider,
                         provider_id=QUANTINUUM_PROVIDER_ID,
                         **kwargs)
