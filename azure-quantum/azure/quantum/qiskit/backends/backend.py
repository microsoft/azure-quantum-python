##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import json

import logging
import warnings

logger = logging.getLogger(__name__)

from typing import Any, Dict, Tuple, Union, List
from azure.quantum.version import __version__
from azure.quantum.qiskit.job import (
    MICROSOFT_OUTPUT_DATA_FORMAT,
    MICROSOFT_OUTPUT_DATA_FORMAT_V2,
    AzureQuantumJob,
)
from abc import abstractmethod

try:
    from qiskit import QuantumCircuit, transpile
    from qiskit.providers import BackendV1 as Backend
    from qiskit.providers import Options
    from qiskit.providers import Provider
    from qiskit.providers.models import BackendConfiguration
    from qiskit.qobj import Qobj, QasmQobj

except ImportError:
    raise ImportError(
        "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
    )


class AzureBackendBase(Backend):
    @abstractmethod
    def __init__(
        self, configuration: BackendConfiguration, provider: Provider = None, **fields
    ):
        super().__init__(configuration, provider, **fields)

    @classmethod
    @abstractmethod
    def _default_options(cls) -> Options:
        pass

    @abstractmethod
    def _azure_config(self) -> Dict[str, str]:
        pass

    def retrieve_job(self, job_id) -> AzureQuantumJob:
        """Returns the Job instance associated with the given id."""
        return self._provider.get_job(job_id)

    def _get_output_data_format(self, **options) -> str:
        config: BackendConfiguration = self.configuration()
        # output data format default depends on the number of experiments. QIR backends
        # that don't define a default in their azure config will use this value
        # Once more than one experiment is supported, we should always use the v2 format
        default_output_data_format = (
            MICROSOFT_OUTPUT_DATA_FORMAT
            if config.max_experiments == 1
            else MICROSOFT_OUTPUT_DATA_FORMAT_V2
        )

        azure_config: Dict[str, Any] = config.azure
        # if the backend defines an output format, use that over the default
        azure_defined_override = azure_config.get(
            "output_data_format", default_output_data_format
        )
        # if the user specifies an output format, use that over the default azure config
        output_data_format = options.pop("output_data_format", azure_defined_override)

        return output_data_format

    def _get_input_params(self, **options) -> Dict[str, Any]:
        # Backend options are mapped to input_params.
        input_params: Dict[str, Any] = vars(self.options).copy()

        # The shots/count number can be specified in different ways for different providers,
        # so let's get it first. Values in 'kwargs' take precedence over options, and to keep
        # the convention, 'count' takes precedence over 'shots' afterwards.
        shots_count = (
            options["count"]
            if "count" in options
            else options["shots"]
            if "shots" in options
            else input_params["count"]
            if "count" in input_params
            else input_params["shots"]
            if "shots" in input_params
            else None
        )

        # Let's clear the options of both properties regardless of which one was used to prevent
        # double specification of the value.
        options.pop("shots", None)
        options.pop("count", None)

        # Take also into consideration options passed in the options, as the take precedence
        # over default values:
        for opt in options.copy():
            if opt in input_params:
                input_params[opt] = options.pop(opt)

        input_params["count"] = shots_count
        input_params["shots"] = shots_count

        return input_params

    def _run(self, job_name, input_data, input_params, metadata, **options):
        logger.info(f"Submitting new job for backend {self.name()}")

        # The default of these job parameters come from the AzureBackend configuration:
        config = self.configuration()
        blob_name = options.pop("blob_name", config.azure["blob_name"])
        content_type = options.pop("content_type", config.azure["content_type"])
        provider_id = options.pop("provider_id", config.azure["provider_id"])
        input_data_format = options.pop(
            "input_data_format", config.azure["input_data_format"]
        )
        output_data_format = self._get_output_data_format(**options)

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
            input_params=input_params,
            metadata=metadata,
            **options,
        )

        return job

    def _normalize_run_input_params(self, run_input, **options):
        if "circuit" not in options:
            # circuit is not provided, check if there is run_input
            if run_input:
                return run_input
            else:
                raise ValueError("No input provided.")

        if run_input:
            # even though circuit is provided, we still have run_input
            warnings.warn(DeprecationWarning("The circuit parameter has been deprecated and will be ignored."))
            return run_input
        else:
            warnings.warn(DeprecationWarning("The circuit parameter has been deprecated. Please use the run_input parameter."))

        # we don't have run_input
        # we know we have circuit parameter, but it may be empty
        circuit = options.get("circuit")
        
        if circuit:
            return circuit
        else:
            raise ValueError("No input provided.")


class AzureQirBackend(AzureBackendBase):
    @abstractmethod
    def __init__(
        self, configuration: BackendConfiguration, provider: Provider = None, **fields
    ):
        super().__init__(configuration, provider, **fields)

    def _azure_config(self) -> Dict[str, str]:
        return {
            "blob_name": "inputData",
            "content_type": "qir.v1",
            "input_data_format": "qir.v1",
        }

    def run(
        self, run_input: Union[QuantumCircuit, List[QuantumCircuit]] = [], **options
    ) -> AzureQuantumJob:
        """Run on the backend.

        This method returns a 
        :class:`~azure.quantum.qiskit.job.AzureQuantumJob` object
        that runs circuits. This is an async call.

        Args:
            run_input (QuantumCircuit or List[QuantumCircuit]): An individual or a
            list of :class:`~qiskit.circuits.QuantumCircuit` to run on the backend.
              
            options: Any kwarg options to pass to the backend for running the
            config. If a key is also present in the options
            attribute/object then the expectation is that the value
            specified will be used instead of what's set in the options
            object.

        Returns:
            Job: The job object for the run
        """
        run_input = self._normalize_run_input_params(run_input, **options)
        options.pop("run_input", None)
        options.pop("circuit", None)

        circuits = list([])
        if isinstance(run_input, QuantumCircuit):
            circuits = [run_input]
        else:
            circuits = run_input

        max_circuits_per_job = self.configuration().max_experiments
        if len(circuits) > max_circuits_per_job:
            raise NotImplementedError(
                f"This backend only supports running a maximum of {max_circuits_per_job} circuits per job."
            )

        # config normalization
        input_params = self._get_input_params(**options)

        shots_count = input_params["count"]

        job_name = ""
        if len(circuits) > 1:
            job_name = f"batch-{len(circuits)}-{shots_count}"
        else:
            job_name = circuits[0].name
        job_name = options.pop("job_name", job_name)

        metadata = options.pop("metadata", {})

        input_data = self._translate_input(circuits, input_params)

        job = super()._run(job_name, input_data, input_params, metadata, **options)
        logger.info(
            f"Submitted job with id '{job.id()}' with shot count of {shots_count}:"
        )

        return job

    def _generate_qir(
        self, circuits, targetCapability, **to_qir_kwargs
    ) -> Tuple[bytes, List[str]]:
        from qiskit_qir import to_qir_bitcode_with_entry_points

        config = self.configuration()
        # Barriers aren't removed by transpilation and must be explicitly removed in the Qiskit to QIR translation.
        emit_barrier_calls = "barrier" in config.basis_gates
        return to_qir_bitcode_with_entry_points(
            circuits,
            targetCapability,
            emit_barrier_calls=emit_barrier_calls,
            **to_qir_kwargs,
        )

    def _get_qir_str(self, circuits, targetCapability, **to_qir_kwargs) -> str:
        from pyqir import Module

        input_data, _ = self._generate_qir(circuits, targetCapability, **to_qir_kwargs)
        return str(Module.from_bitcode(input_data))

    def _translate_input(
        self, circuits: List[QuantumCircuit], input_params: Dict[str, Any]
    ) -> bytes:
        """Translates the input values to the QIR expected by the Backend."""
        logger.info(f"Using QIR as the job's payload format.")
        config = self.configuration()

        # Override QIR translation parameters
        # We will record the output by default, but allow the backend to override this, and allow the user to override the backend.
        to_qir_kwargs = input_params.pop(
            "to_qir_kwargs", config.azure.get("to_qir_kwargs", {"record_output": True})
        )
        targetCapability = input_params.pop(
            "targetCapability",
            self.options.get("targetCapability", "AdaptiveExecution"),
        )

        if logger.isEnabledFor(logging.DEBUG):
            qir = self._get_qir_str(circuits, targetCapability, **to_qir_kwargs)
            logger.debug(f"QIR:\n{qir}")

        # We'll transpile automatically to the supported gates in QIR unless explicitly skipped.
        if not input_params.pop("skipTranspile", False):
            # Set of gates supported by QIR targets.
            circuits = transpile(
                circuits, basis_gates=config.basis_gates, optimization_level=0
            )
            # We'll only log the QIR again if we performed a transpilation.
            if logger.isEnabledFor(logging.DEBUG):
                qir = self._get_qir_str(circuits, targetCapability, **to_qir_kwargs)
                logger.debug(f"QIR (Post-transpilation):\n{qir}")

        (input_data, entry_points) = self._generate_qir(
            circuits, targetCapability, **to_qir_kwargs
        )

        arguments = input_params.pop("arguments", [])
        input_params["items"] = [
            {"entryPoint": name, "arguments": arguments} for name in entry_points
        ]

        return input_data


class AzureBackend(AzureBackendBase):
    """Base class for interfacing with a backend in Azure Quantum"""

    @abstractmethod
    def __init__(
        self, configuration: BackendConfiguration, provider: Provider = None, **fields
    ):
        super().__init__(configuration, provider, **fields)

    backend_name = None

    def _prepare_job_metadata(self, circuit):
        """Returns the metadata relative to the given circuit that will be attached to the Job"""
        return {
            "qiskit": True,
            "name": circuit.name,
            "num_qubits": circuit.num_qubits,
            "metadata": json.dumps(circuit.metadata),
        }

    @abstractmethod
    def _translate_input(self, circuit):
        pass

    def run(self, run_input = None, **kwargs):
        """Submits the given circuit to run on an Azure Quantum backend."""
        options = kwargs
        circuit = self._normalize_run_input_params(run_input, **options)
        options.pop("run_input", None)
        options.pop("circuit", None)
        
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
            if options.get("shots") is None:
                # Note that the default number of shots for QObj is 1024
                # unless the user specifies the backend.
                options["shots"] = run["shots"]

        # If not provided as options, the values of these parameters
        # are calculated from the circuit itself:
        job_name = options.pop("job_name", circuit.name)
        metadata = options.pop("metadata", self._prepare_job_metadata(circuit))

        input_params = self._get_input_params(**options)

        input_data = self._translate_input(circuit)

        job = super()._run(job_name, input_data, input_params, metadata, **options)

        shots_count = input_params["count"]
        logger.info(
            f"Submitted job with id '{job.id()}' for circuit '{circuit.name}' with shot count of {shots_count}:"
        )
        logger.info(input_data)

        return job
