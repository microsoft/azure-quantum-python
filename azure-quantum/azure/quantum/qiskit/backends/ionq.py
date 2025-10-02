##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from typing import TYPE_CHECKING, Dict, List, Union
from azure.quantum import __version__
from azure.quantum.qiskit.job import AzureQuantumJob
from azure.quantum.target.ionq import IonQ
from abc import abstractmethod
from qsharp import TargetProfile
from qiskit import QuantumCircuit

from .backend import (
    AzureBackend, 
    AzureQirBackend, 
    _get_shots_or_deprecated_count_input_param
)

from qiskit.providers.models import BackendConfiguration
from qiskit.providers import Options, Provider

from qiskit_ionq.helpers import (
    GATESET_MAP,
    qiskit_circ_to_ionq_circ,
)

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

import json

import logging

logger = logging.getLogger(__name__)

__all__ = [
    "IonQBackend",
    "IonQSimulatorBackend",
    "IonQAriaBackend",
    "IonQForteBackend",
    "IonQQirBackend",
    "IonQSimulatorQirBackend",
    "IonQSimulatorNativeBackend",
    "IonQAriaQirBackend",
    "IonQForteQirBackend",
    "IonQAriaNativeBackend",
    "IonQForteNativeBackend",
]

_IONQ_SHOTS_INPUT_PARAM_NAME = "shots"
_DEFAULT_SHOTS_COUNT = 500

class IonQQirBackendBase(AzureQirBackend):
    """Base class for interfacing with an IonQ QIR backend"""

    _SHOTS_PARAM_NAME = _IONQ_SHOTS_INPUT_PARAM_NAME

    @abstractmethod
    def __init__(
        self, configuration: BackendConfiguration, provider: Provider = None, **fields
    ):
        super().__init__(configuration, provider, **fields)

    @classmethod
    def _default_options(cls) -> Options:
        return Options(
            **{
                cls._SHOTS_PARAM_NAME: _DEFAULT_SHOTS_COUNT,
            },
            target_profile=TargetProfile.Base,
            )

    def _azure_config(self) -> Dict[str, str]:
        config = super()._azure_config()
        config.update(
            {
                "provider_id": "ionq",
            }
        )
        return config

    def run(
        self, 
        run_input: Union[QuantumCircuit, List[QuantumCircuit]] = [],
        shots: int = None,
        **options,
    ) -> AzureQuantumJob:
        
        # In earlier versions, backends for all providers accepted the 'count' option,
        # but now we accept it only for a compatibility reasons and do not recommend using it.
        count = options.pop("count", None)

        final_shots = _get_shots_or_deprecated_count_input_param(
            param_name=self.__class__._SHOTS_PARAM_NAME,
            shots=shots,
            count=count,
        )
        
        return super().run(run_input, shots=final_shots, **options)


class IonQSimulatorQirBackend(IonQQirBackendBase):
    backend_names = ("ionq.simulator",)

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an IonQ QIR Simulator backend"""
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "IonQ simulator on Azure Quantum",
                "basis_gates": self._basis_gates(),
                "memory": False,
                "n_qubits": 29,
                "conditional": False,
                "max_shots": None,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        logger.info("Initializing IonQSimulatorQirBackend")
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class IonQAriaQirBackend(IonQQirBackendBase):
    backend_names = ("ionq.qpu.aria-1",)

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an IonQ Aria QPU backend"""
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "IonQ Aria QPU on Azure Quantum",
                "basis_gates": self._basis_gates(),
                "memory": False,
                "n_qubits": 25,
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        logger.info("Initializing IonQAriaQirBackend")
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class IonQForteQirBackend(IonQQirBackendBase):
    backend_names = ("ionq.qpu.forte-1","ionq.qpu.forte-enterprise-1",)

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an IonQ Forte QPU backend"""
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "IonQ Forte QPU on Azure Quantum",
                "basis_gates": self._basis_gates(),
                "memory": False,
                "n_qubits": 35,
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
            }
        )
        logger.info("Initializing IonQForteQirBackend")
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class IonQBackend(AzureBackend):
    """Base class for interfacing with an IonQ backend in Azure Quantum"""

    backend_name = None

    _SHOTS_PARAM_NAME = _IONQ_SHOTS_INPUT_PARAM_NAME

    @abstractmethod
    def __init__(
        self, configuration: BackendConfiguration, provider: Provider = None, **fields
    ):
        super().__init__(configuration, provider, **fields)

    def run(
        self, 
        run_input=None,
        shots: int = None,
        **options,
    ) -> AzureQuantumJob:
        
        # In earlier versions, backends for all providers accepted the 'count' option,
        # but now we accept it only for a compatibility reasons and do not recommend using it.
        count = options.pop("count", None)

        final_shots = _get_shots_or_deprecated_count_input_param(
            param_name=self.__class__._SHOTS_PARAM_NAME,
            shots=shots,
            count=count,
        )
        
        return super().run(run_input, shots=final_shots, **options)

    @classmethod
    def _default_options(cls):
        return Options(
            **{
                cls._SHOTS_PARAM_NAME: _DEFAULT_SHOTS_COUNT,
            },
        )

    def _azure_config(self) -> Dict[str, str]:
        return {
            "blob_name": "inputData",
            "content_type": "application/json",
            "provider_id": "ionq",
            "input_data_format": "ionq.circuit.v1",
            "output_data_format": "ionq.quantum-results.v1",
            "is_default": False,
        }

    def _prepare_job_metadata(self, circuit, **kwargs):
        _, _, meas_map = qiskit_circ_to_ionq_circ(circuit, gateset=self.gateset())

        metadata = super()._prepare_job_metadata(circuit, **kwargs)
        metadata["meas_map"] = json.dumps(meas_map)

        return metadata

    def _translate_input(self, circuit):
        """Translates the input values to the format expected by the AzureBackend."""
        ionq_circ, _, _ = qiskit_circ_to_ionq_circ(circuit, gateset=self.gateset())
        input_data = {
            "gateset": self.gateset(),
            "qubits": circuit.num_qubits,
            "circuit": ionq_circ,
        }
        return IonQ._encode_input_data(input_data)

    def gateset(self):
        return self.configuration().gateset


class IonQSimulatorBackend(IonQBackend):
    backend_names = ("ionq.simulator",)

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an IonQ Simulator backend"""
        gateset = kwargs.pop("gateset", "qis")
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "IonQ simulator on Azure Quantum",
                "basis_gates": GATESET_MAP[gateset],
                "memory": False,
                "n_qubits": 29,
                "conditional": False,
                "max_shots": None,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
                "gateset": gateset,
            }
        )
        logger.info("Initializing IonQSimulatorBackend")
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class IonQSimulatorNativeBackend(IonQSimulatorBackend):
    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        if "gateset" not in kwargs:
            kwargs["gateset"] = "native"
        super().__init__(name, provider, **kwargs)


class IonQAriaBackend(IonQBackend):
    backend_names = ("ionq.qpu.aria-1",)

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an IonQ Aria QPU backend"""
        gateset = kwargs.pop("gateset", "qis")
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "IonQ Aria QPU on Azure Quantum",
                "basis_gates": GATESET_MAP[gateset],
                "memory": False,
                "n_qubits": 23,
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
                "gateset": gateset,
            }
        )
        logger.info("Initializing IonQAriaQPUBackend")
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class IonQForteBackend(IonQBackend):
    backend_names = ("ionq.qpu.forte-1","ionq.qpu.forte-enterprise-1",)

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Base class for interfacing with an IonQ Forte QPU backend"""
        gateset = kwargs.pop("gateset", "qis")
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "IonQ Forte QPU on Azure Quantum",
                "basis_gates": GATESET_MAP[gateset],
                "memory": False,
                "n_qubits": 35,
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
                "azure": self._azure_config(),
                "gateset": gateset,
            }
        )
        logger.info("Initializing IonQForteBackend")
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class IonQAriaNativeBackend(IonQAriaBackend):
    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        if "gateset" not in kwargs:
            kwargs["gateset"] = "native"
        super().__init__(name, provider, **kwargs)


class IonQForteNativeBackend(IonQForteBackend):
    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        if "gateset" not in kwargs:
            kwargs["gateset"] = "native"
        super().__init__(name, provider, **kwargs)
