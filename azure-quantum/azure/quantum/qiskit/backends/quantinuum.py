##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import warnings

from typing import TYPE_CHECKING, Union, List
from azure.quantum.version import __version__
from azure.quantum.qiskit.job import AzureQuantumJob

from .backend import AzureBackend

from qiskit import QuantumCircuit
from qiskit.providers.models import BackendConfiguration
from qiskit.providers import Options

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

import logging
logger = logging.getLogger(__name__)

__all__ = [
    "QuantinuumBackend",
    "QuantinuumQPUBackend",
    "QuantinuumSyntaxCheckerBackend",
    "QuantinuumEmulatorBackend"
]

QUANTINUUM_BASIS_GATES = [
    "x",
    "y",
    "z",
    "rx",
    "ry",
    "rz",
    "h",
    "cx",
    "ccx",
    "cz",
    "s",
    "sdg",
    "t",
    "tdg",
    "v",
    "vdg",
    "zz",
    "measure",
    "reset"
]

QUANTINUUM_PROVIDER_ID = "quantinuum"
QUANTINUUM_PROVIDER_NAME = "Quantinuum"

class QuantinuumBackend(AzureBackend):
    """Base class for interfacing with a Quantinuum (formerly Honeywell) backend in Azure Quantum"""

    def __init__(self, **kwargs):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME
        super().__init__(**kwargs)

    @classmethod
    def _default_options(cls):
        return Options(count=500, targetCapability="openqasm")

    def _azure_config(self):
        return {
            "blob_name": "inputData",
            "content_type": "application/qasm",
            "provider_id": self._provider_id,
            "input_data_format": "honeywell.openqasm.v1",
            "output_data_format": "honeywell.quantum-results.v1",
        }

    def _translate_input(self, circuit, data_format, input_params, to_qir_kwargs={}):
        """ Translates the input values to the format expected by the AzureBackend. """
        if input_params["targetCapability"] == "openqasm":
            return (circuit.qasm(), data_format, input_params)
        else:
            # Not using openqasm, assume qir then:
            return super()._translate_input(circuit, "qir.v1", input_params, to_qir_kwargs)

    def _initialize_n_qubits(self, name):
        name = name.lower()
        self.n_qubits = 20 if "h1-1" in name or "s1" in name else 12
        return self.n_qubits

    def estimate_cost(self, circuit: QuantumCircuit, shots: int = None, count: int = None):
        """Estimate cost for running this circuit

        :param circuit: Qiskit quantum circuit
        :type circuit: QuantumCircuit
        :param shots: Shot count
        :type shots: int
        :param count: Shot count (alternative to 'shots')
        :type count: int
        """
        if count is not None:
            shots = count

        if shots is None:
            raise ValueError("Missing input argument 'shots'.")

        input_data = circuit.qasm()
        workspace = self.provider().get_workspace()
        target = workspace.get_targets(self.name())
        return target.estimate_cost(input_data, num_shots=shots)


class QuantinuumSyntaxCheckerBackend(QuantinuumBackend):
    backend_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.hqs-lt-s1-apival", "quantinuum.sim.h1-1sc",
        "quantinuum.hqs-lt-s2-apival", "quantinuum.sim.h1-2sc"
    )

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME

        self._initialize_n_qubits(name)
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": f"Quantinuum Syntax Checker on Azure Quantum",
                "basis_gates": QUANTINUUM_BASIS_GATES,
                "memory": False,
                "n_qubits": self.n_qubits,
                "conditional": False,
                "max_shots": None,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        logger.info(f"Initializing {self._provider_name}SyntaxCheckerBackend")
        super().__init__(configuration=configuration,
                         provider=provider,
                         **kwargs)


class QuantinuumEmulatorBackend(QuantinuumBackend):
    backend_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.hqs-lt-s1-sim", "quantinuum.sim.h1-1e",
        "quantinuum.hqs-lt-s2-sim", "quantinuum.sim.h1-2e"
    )

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME

        self._initialize_n_qubits(name)
        configuration: BackendConfiguration = kwargs.pop("configuration", None)
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": f"Quantinuum emulator on Azure Quantum",
                "basis_gates": QUANTINUUM_BASIS_GATES,
                "memory": False,
                "n_qubits": self.n_qubits,
                "conditional": False,
                "max_shots": None,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        logger.info(f"Initializing {self._provider_name}EmulatorBackend")
        super().__init__(configuration=configuration,
                         provider=provider,
                         **kwargs)


class QuantinuumQPUBackend(QuantinuumBackend):
    backend_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.hqs-lt-s1", "quantinuum.qpu.h1-1",
        "quantinuum.hqs-lt-s2", "quantinuum.qpu.h1-2"
    )

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        self._provider_id = QUANTINUUM_PROVIDER_ID
        self._provider_name = QUANTINUUM_PROVIDER_NAME

        self._initialize_n_qubits(name)
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": f"Quantinuum QPU on Azure Quantum",
                "basis_gates": QUANTINUUM_BASIS_GATES,
                "memory": False,
                "n_qubits": self.n_qubits,
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        logger.info(f"Initializing {self._provider_name}QPUBackend")
        super().__init__(configuration=configuration,
                         provider=provider,
                         **kwargs)
