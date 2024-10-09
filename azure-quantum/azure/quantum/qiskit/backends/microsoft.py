##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##

from typing import TYPE_CHECKING, Any, Dict, List, Union
from azure.quantum.version import __version__
from qiskit import QuantumCircuit
from abc import abstractmethod
from .backend import AzureQirBackend, QIR_BASIS_GATES

from qiskit.providers.models import BackendConfiguration
from qiskit.providers import Options, Provider
from qsharp import TargetProfile
from qsharp.interop.qiskit import ResourceEstimatorBackend
import pyqir as pyqir

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

import logging

logger = logging.getLogger(__name__)

__all__ = ["MicrosoftBackend", "MicrosoftResourceEstimationBackend"]


class MicrosoftBackend(AzureQirBackend):
    """Base class for interfacing with a Microsoft backend in Azure Quantum"""

    @abstractmethod
    def __init__(
        self, configuration: BackendConfiguration, provider: Provider = None, **fields
    ):
        super().__init__(configuration, provider, **fields)

    @classmethod
    def _default_options(cls):
        return Options(target_profile=TargetProfile.Adaptive_RI)

    def _azure_config(self) -> Dict[str, str]:
        config = super()._azure_config()
        config.update(
            {
                "provider_id": "microsoft-qc",
                "output_data_format": "microsoft.resource-estimates.v1",
            }
        )
        return config

    def _translate_input(
        self,
        circuits: Union[QuantumCircuit, List[QuantumCircuit]],
        input_params: Dict[str, Any],
    ) -> bytes:
        """Translates the input values to the QIR expected by the Backend."""
        # All the logic is in the base class, but we need to override
        # this method to ensure that the bitcode QIR format is used for RE.

        # normal translation is to QIR text format in utf-8 encoded bytes
        ir_byte_str = super()._translate_input(circuits, input_params)
        # decode the utf-8 encoded bytes to a string
        ir_str = ir_byte_str.decode('utf-8')
        # convert the QIR text format to QIR bitcode format
        module = pyqir.Module.from_ir(pyqir.Context(), ir_str)
        return module.bitcode

    def _generate_qir(
        self, circuits: List[QuantumCircuit], target_profile: TargetProfile, **kwargs
    ) -> pyqir.Module:
        if len(circuits) == 0:
            raise ValueError("No QuantumCircuits provided")

        name = "circuits"
        if isinstance(circuits, QuantumCircuit):
            name = circuits.name
            circuits = [circuits]
        elif isinstance(circuits, list):
            for value in circuits:
                if not isinstance(value, QuantumCircuit):
                    raise ValueError(
                        "Input must be Union[QuantumCircuit, List[QuantumCircuit]]"
                    )
        else:
            raise ValueError(
                "Input must be Union[QuantumCircuit, List[QuantumCircuit]]"
            )

        skip_transpilation = kwargs.pop("skip_transpilation", False)
        backend = ResourceEstimatorBackend(
            skip_transpilation=skip_transpilation, **kwargs
        )
        context = pyqir.Context()
        llvm_module = pyqir.qir_module(context, name)
        for circuit in circuits:
            qir_str = backend.qir(circuit, target_profile=target_profile)
            module = pyqir.Module.from_ir(context, qir_str)
            llvm_module.link(module)

        err = llvm_module.verify()
        if err is not None:
            raise Exception(err)

        return llvm_module


class MicrosoftResourceEstimationBackend(MicrosoftBackend):
    """Backend class for interfacing with the resource estimator target"""

    backend_names = ("microsoft.estimator",)

    @classmethod
    def _default_options(cls):
        return Options(
            target_profile=TargetProfile.Adaptive_RI,
            errorBudget=1e-3,
            qubitParams={"name": "qubit_gate_ns_e3"},
            qecScheme={"name": "surface_code"}
        )

    def __init__(self, name: str, provider: "AzureQuantumProvider", **kwargs):
        """Constructor for class to interface with the resource estimator target"""
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "Resource estimator on Azure Quantum",
                "basis_gates": QIR_BASIS_GATES,
                "memory": False,
                "n_qubits": 0xFFFFFFFFFFFFFFFF,  # NOTE: maximum 64-bit unsigned value
                "conditional": True,
                "max_shots": 1,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [
                    {"name": "TODO", "parameters": [], "qasm_def": "TODO"}
                ],  # NOTE: copied from other backends
                "azure": self._azure_config(),
                "is_default": True,
            }
        )
        logger.info("Initializing MicrosoftResourceEstimationBackend")
        configuration: BackendConfiguration = kwargs.pop(
            "configuration", default_config
        )
        super().__init__(configuration=configuration, provider=provider, **kwargs)
