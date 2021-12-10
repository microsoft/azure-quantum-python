##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import json
from typing import TYPE_CHECKING
from azure.quantum import __version__
from azure.quantum.qiskit.job import AzureQuantumJob

try:
    from qiskit.providers import BackendV1 as Backend
    from qiskit.providers.models import BackendConfiguration
    from qiskit.providers import Options
    from qiskit.qobj import Qobj, QasmQobj

    from qiskit_ionq.helpers import ionq_basis_gates, qiskit_circ_to_ionq_circ
except ImportError:
    raise ImportError(
    "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
)

if TYPE_CHECKING:
    from azure.quantum.qiskit import AzureQuantumProvider

import logging
logger = logging.getLogger(__name__)

__all__ = ["IonQBackend", "IonQQPUBackend", "IonQSimulatorBackend"]


class IonQBackend(Backend):
    """Base class for interfacing with an IonQ backend in Azure Quantum"""
    backend_name = None

    @classmethod
    def _default_options(cls):
        return Options(shots=500)

    def _job_metadata(self, circuit, meas_map):
        return {
            "qiskit": True,
            "name": circuit.name,
            "num_qubits": circuit.num_qubits,
            "meas_map": meas_map,
        }

    @staticmethod
    def _translate_circuit(circuit, **kwargs):
        ionq_circ, _, meas_map = qiskit_circ_to_ionq_circ(circuit)
        input_data = {
            "qubits": circuit.num_qubits,
            "circuit": ionq_circ,
        }

        return input_data, meas_map

    def estimate_price(self, circuit, shots):
        """Estimate the price for the given circuit."""
        input_data, _ = self._translate_circuit(circuit)
        workspace = self.provider().get_workspace()
        target = workspace.get_targets(self.name())
        return target.estimate_price(input_data, num_shots=shots)

    def run(self, circuit, **kwargs):
        """Submits the given circuit to run on an IonQ target."""
        # If the circuit was created using qiskit.assemble,
        # disassemble into QASM here
        if isinstance(circuit, QasmQobj) or isinstance(circuit, Qobj):
            from qiskit.assembler import disassemble
            circuits, run, _ = disassemble(circuit)
            circuit = circuits[0]
            if kwargs.get("shots") is None:
                # Note that the default number of shots for QObj is 1024
                # unless the user specifies the backend.
                kwargs["shots"] = run["shots"]

        input_data, meas_map = self._translate_circuit(circuit, **kwargs)

        # Options are mapped to input_params
        # Take also into consideration options passed in the kwargs, as the take precedence
        # over default values:
        input_params = vars(self.options)
        for opt in kwargs.copy():
            if opt in input_params:
                input_params[opt] = kwargs.pop(opt)

        logger.info(f"Submitting new job for basckend {self.name()}")
        job = AzureQuantumJob(
            backend=self,
            name=circuit.name,
            target=self.name(),
            input_data=json.dumps(input_data),
            blob_name="inputData",
            content_type="application/json",
            provider_id="ionq",
            input_data_format="ionq.circuit.v1",
            output_data_format="ionq.quantum-results.v1",
            input_params = input_params,
            metadata= self._job_metadata(circuit=circuit, meas_map=meas_map),
            **kwargs
        )

        logger.info(f"Submitted job with id '{job.id()}' for circuit '{circuit.name}':")
        logger.info(input_data)

        return job

    def retrieve_job(self, job_id) -> AzureQuantumJob:
        """ Returns the Job instance associated with the given id."""
        return self._provider.get_job(job_id)


class IonQSimulatorBackend(IonQBackend):
    backend_names = ("ionq.simulator",)

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        """Base class for interfacing with an IonQ Simulator backend"""
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": True,
                "local": False,
                "coupling_map": None,
                "description": "IonQ simulator on Azure Quantum",
                "basis_gates": ionq_basis_gates,
                "memory": False,
                "n_qubits": 29,
                "conditional": False,
                "max_shots": 1,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
            }
        )
        logger.info("Initializing IonQSimulatorBackend")
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        super().__init__(configuration=configuration, provider=provider, **kwargs)


class IonQQPUBackend(IonQBackend):
    backend_names = ("ionq.qpu",)

    def __init__(
        self,
        name: str,
        provider: "AzureQuantumProvider",
        **kwargs
    ):
        """Base class for interfacing with an IonQ QPU backend"""
        default_config = BackendConfiguration.from_dict(
            {
                "backend_name": name,
                "backend_version": __version__,
                "simulator": False,
                "local": False,
                "coupling_map": None,
                "description": "IonQ QPU on Azure Quantum",
                "basis_gates": ionq_basis_gates,
                "memory": False,
                "n_qubits": 11,
                "conditional": False,
                "max_shots": 10000,
                "max_experiments": 1,
                "open_pulse": False,
                "gates": [{"name": "TODO", "parameters": [], "qasm_def": "TODO"}],
            }
        )
        logger.info("Initializing IonQQPUBackend")
        configuration: BackendConfiguration = kwargs.pop("configuration", default_config)
        super().__init__(configuration=configuration, provider=provider, **kwargs)
