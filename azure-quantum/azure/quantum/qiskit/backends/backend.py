##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import warnings
import json

import logging
logger = logging.getLogger(__name__)

from typing import TYPE_CHECKING, Union, List
from azure.quantum.version import __version__
from azure.quantum.qiskit.job import AzureQuantumJob

try:
    from qiskit import QuantumCircuit
    from qiskit.providers import BackendV1 as Backend
    from qiskit.qobj import Qobj, QasmQobj

except ImportError:
    raise ImportError(
    "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
)

# Set of gates supported by QIR targets.
QIR_BASIS_GATES = [
    "x",
    "y",
    "z",
    "rx",
    "ry",
    "rz",
    "h",
    "cx",
    "cz",
    "s",
    "sdg",
    "t",
    "tdg",
    "measure",
    "reset"
]

class AzureBackend(Backend):
    """Base class for interfacing with an IonQ backend in Azure Quantum"""
    backend_name = None

    def _job_metadata(self, circuit, **kwargs):
        """ Returns the metadata relative to the given circuit that will be attached to the Job"""

        return {
            "qiskit": True,
            "name": circuit.name,
            "num_qubits": circuit.num_qubits,
            "metadata": json.dumps(circuit.metadata),
        }

    def _translate_circuit(self, circuit, input_data_format, **kwargs):
        """ Translates the circuit to the format expected by the AzureBackend. """
        return NotImplementedError("AzureBackends must implement _translate_circuit.")


    def _to_qir(self, circuit, **kwargs):
        """ Translates the circuit to the format expected by the AzureBackend. """
        logger.info(f"Using QIR as the job's payload format.")
        from qiskit_qir import to_qir_bitcode, to_qir

        input_data = bytes(to_qir_bitcode(circuit))
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"QIR:\n{to_qir(circuit)}")

        return (input_data, {"entryPoint": "main", "arguments": []})


    def run(self, circuit, **kwargs):
        """Submits the given circuit to run on an Azure Quantum backend."""        

        # Some Qiskit features require passing lists of circuits, so unpack those here.
        # We currently only support single-experiment jobs.
        if isinstance(circuit, (list, tuple)):
            if len(circuit) > 1:
                raise NotImplementedError("Multi-experiment jobs are not supported!")
            circuit = circuit[0]

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
        
        # The default of these job parameters come from the AzureBackend configuration:
        config = self.configuration()
        blob_name = kwargs.pop("blob_name", config.azure["blob_name"])
        content_type = kwargs.pop("content_type", config.azure["content_type"])
        provider_id = kwargs.pop("provider_id", config.azure["provider_id"])
        input_data_format = kwargs.pop("input_data_format", config.azure["input_data_format"])
        output_data_format = kwargs.pop("output_data_format", config.azure["output_data_format"])

        # If not provided as kwargs, the values of these parameters 
        # are calculated from the circuit itself:
        job_name = kwargs.pop("job_name", circuit.name)
        metadata = kwargs.pop("metadata") if "metadata" in kwargs else self._job_metadata(circuit, **kwargs)

        # Backend options are mapped to input_params.
        # Take also into consideration options passed in the kwargs, as the take precedence
        # over default values:
        input_params = vars(self.options)
        for opt in kwargs.copy():
            if opt in input_params:
                input_params[opt] = kwargs.pop(opt)
        
        # Select method to encode payload based on input_data_format
        if input_data_format == "qir.v1":
            input_data, arguments = self._to_qir(circuit, **kwargs)
            for a in arguments.keys():
                input_params[a] = arguments[a]
        else:
            input_data = self._translate_circuit(circuit, input_data_format, **kwargs)

        logger.info(f"Submitting new job for backend {self.name()}")
        job = AzureQuantumJob(
            backend=self,
            target=self.name(),
            name=job_name,
            input_data=input_data,
            blob_name=blob_name,
            content_type=content_type,
            provider_id=provider_id,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            input_params = input_params,
            metadata=metadata,
            **kwargs
        )

        logger.info(f"Submitted job with id '{job.id()}' for circuit '{circuit.name}':")
        logger.info(input_data)

        return job

    def retrieve_job(self, job_id) -> AzureQuantumJob:
        """ Returns the Job instance associated with the given id."""
        return self._provider.get_job(job_id)
