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

    def _prepare_job_metadata(self, circuit):
        """ Returns the metadata relative to the given circuit that will be attached to the Job"""
        return {
            "qiskit": True,
            "name": circuit.name,
            "num_qubits": circuit.num_qubits,
            "metadata": json.dumps(circuit.metadata),
        }

    def _translate_input(self, circuit, data_format, input_params):
        """ Translates the input values to the format expected by the AzureBackend. """
        if data_format != "qir.v1":
            target = self.name()
            raise ValueError(f"{data_format} is not a supported data format for target {target}.")

        logger.info(f"Using QIR as the job's payload format.")
        from qiskit_qir import to_qir_bitcode, to_qir

        capability = input_params["targetCapability"] if "targetCapability" in input_params else "AdaptiveProfileExecution"

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"QIR:\n{to_qir(circuit, capability)}")

        # all qir payload needs to define an entryPoint and arguments:
        if not "entryPoint" in input_params:
            input_params["entryPoint"] = "main"
        if not "arguments" in input_params:
            input_params["arguments"] = []

        if input_params.get("auto_transpile", False):
            from qiskit import transpile
            from qiskit_qir import SUPPORTED_INSTRUCTIONS
            circuit = transpile(circuit, basis_gates = SUPPORTED_INSTRUCTIONS)

            # We'll only log the QIR again if we performed a transpilation.
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(f"QIR (Post-transpilation):\n{to_qir(circuit, capability)}")

        qir = bytes(to_qir_bitcode(circuit, capability))
        return (qir, data_format, input_params)

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
        metadata = kwargs.pop("metadata") if "metadata" in kwargs else self._prepare_job_metadata(circuit)

        # Backend options are mapped to input_params.
        # Take also into consideration options passed in the kwargs, as the take precedence
        # over default values:
        input_params = vars(self.options)
        for opt in kwargs.copy():
            if opt in input_params:
                input_params[opt] = kwargs.pop(opt)

        # Some providers refer as 'shots' the 'count' parameter,
        # Remove this once all providers accept "count":
        if "shots" in input_params:
            input_params["count"] = input_params["shots"]

        # By default, we'll transpile into the list of QIR supported instructions
        # unless the user has indicated that this step should be skipped.
        if "skip-qir-auto-transpile" in kwargs:
            input_params["auto_transpile"] = not kwargs.pop("skip-auto-transpile")
        else:
            input_params["auto_transpile"] = True

        # translate
        (input_data, input_data_format, input_params) = self._translate_input(circuit, input_data_format, input_params)

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
