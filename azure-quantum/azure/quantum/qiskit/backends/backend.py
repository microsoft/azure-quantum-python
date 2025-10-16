##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import os
import json

import logging
import warnings

logger = logging.getLogger(__name__)

from typing import Any, Dict, Union, List, Optional
from azure.quantum.version import __version__
from azure.quantum.qiskit.job import (
    MICROSOFT_OUTPUT_DATA_FORMAT,
    MICROSOFT_OUTPUT_DATA_FORMAT_V2,
    AzureQuantumJob,
)
from abc import abstractmethod
from azure.quantum.job.session import SessionHost

try:
    from qiskit import QuantumCircuit
    from qiskit.providers import BackendV1 as Backend
    from qiskit.providers import Options
    from qiskit.providers import Provider
    from qiskit.providers.models import BackendConfiguration
    from qiskit.qobj import QasmQobj, PulseQobj
    from qsharp.interop.qiskit import QSharpBackend
    from qsharp import TargetProfile

except ImportError:
    raise ImportError(
        "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
    )

# barrier is handled by an extra flag which will transpile
# them away if the backend doesn't support them. This has
# to be done as a special pass as the transpiler will not
# remove barriers by default.
QIR_BASIS_GATES = [
    "measure",
    "reset",
    "ccx",
    "cx",
    "cy",
    "cz",
    "rx",
    "rxx",
    "crx",
    "ry",
    "ryy",
    "cry",
    "rz",
    "rzz",
    "crz",
    "h",
    "s",
    "sdg",
    "swap",
    "t",
    "tdg",
    "x",
    "y",
    "z",
    "id",
    "ch",
]


class AzureBackendBase(Backend, SessionHost):

    # Name of the provider's input parameter which specifies number of shots for a submitted job.
    # If None, backend will not pass this input parameter. 
    _SHOTS_PARAM_NAME = None

    @abstractmethod
    def __init__(
        self,
        configuration: BackendConfiguration,
        provider: Provider = None,
        **fields
    ):
        super().__init__(configuration, provider, **fields)
    
    @abstractmethod
    def run(
        self,
        run_input: Union[QuantumCircuit, List[QuantumCircuit]] = [],
        shots: int = None, 
        **options,
    ) -> AzureQuantumJob:
        """Run on the backend.

        This method returns a
        :class:`~azure.quantum.qiskit.job.AzureQuantumJob` object
        that runs circuits. 

        Args:
            run_input (QuantumCircuit or List[QuantumCircuit]): An individual or a
            list of one :class:`~qiskit.circuits.QuantumCircuit` to run on the backend.
            shots (int, optional): Number of shots, defaults to None.
            options: Any kwarg options to pass to the backend for running the
            config. If a key is also present in the options
            attribute/object then the expectation is that the value
            specified will be used instead of what's set in the options
            object.

        Returns:
            Job: The job object for the run
        """
        pass

    @classmethod
    def _can_send_shots_input_param(cls) -> bool:
        """
        Tells if provider's backend class is able to specify shots number for its jobs.
        """
        return cls._SHOTS_PARAM_NAME is not None

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

    def _get_output_data_format(self, options: Dict[str, Any] = {}) -> str:
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
    
    def _get_input_params(self, options: Dict[str, Any], shots: int = None) -> Dict[str, Any]:
        # Backend options are mapped to input_params.
        input_params: Dict[str, Any] = vars(self.options).copy()

        # Determine shots number, if needed.
        if self._can_send_shots_input_param():
            options_shots = options.pop(self.__class__._SHOTS_PARAM_NAME, None)

            final_shots = None
            # First we check for the explicitly specified 'shots' parameter, then for a provider-specific
            # field in options, then for a backend's default value. 

            # Warn about options conflict, default to 'shots'.
            if shots is not None and options_shots is not None:
                warnings.warn(
                    f"Parameter 'shots' conflicts with the '{self.__class__._SHOTS_PARAM_NAME}' parameter. "
                    "Please, provide only one option for setting shots. Defaulting to 'shots' parameter."
                )
                final_shots = shots
            
            elif shots is not None:
                final_shots = shots
            elif options_shots is not None:
                warnings.warn(
                    f"Parameter '{self.__class__._SHOTS_PARAM_NAME}' is subject to change in future versions. "
                    "Please, use 'shots' parameter instead."
                )
                final_shots = options_shots
            
            # If nothing is found, try to get from default values.
            if final_shots is None:
                final_shots = input_params.get(self.__class__._SHOTS_PARAM_NAME)

            # Also add all possible shots options into input_params to make sure 
            # that all backends covered. 
            # TODO: Double check all backends for shots options in order to remove this extra check.
            input_params["shots"] = final_shots
            input_params["count"] = final_shots

            # Safely removing "shots" and "count" from options as they will be passed in input_params now.
            _ = options.pop("shots", None)
            _ = options.pop("count", None)

            input_params[self.__class__._SHOTS_PARAM_NAME] = final_shots
            

        if "items" in options:
            input_params["items"] = options.pop("items")

        # Take also into consideration options passed in the options, as the take precedence
        # over default values:
        for opt in options.copy():
            if opt in input_params:
                input_params[opt] = options.pop(opt)

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
        output_data_format = self._get_output_data_format(options)

        # QIR backends will have popped "targetCapability" to configure QIR generation.
        # Anything left here is an invalid parameter with the user attempting to use
        # deprecated parameters.
        targetCapability = input_params.get("targetCapability", None)
        if (
            targetCapability not in [None, "qasm"]
            and input_data_format != "qir.v1"
        ):
            message = "The targetCapability parameter has been deprecated and is only supported for QIR backends."
            message += os.linesep
            message += "To find a QIR capable backend, use the following code:"
            message += os.linesep
            message += (
                f'\tprovider.get_backend("{self.name()}", input_data_format: "qir.v1").'
            )
            raise ValueError(message)

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
            warnings.warn(
                DeprecationWarning(
                    "The circuit parameter has been deprecated and will be ignored."
                )
            )
            return run_input
        else:
            warnings.warn(
                DeprecationWarning(
                    "The circuit parameter has been deprecated. Please use the run_input parameter."
                )
            )

        # we don't have run_input
        # we know we have circuit parameter, but it may be empty
        circuit = options.get("circuit")

        if circuit:
            return circuit
        else:
            raise ValueError("No input provided.")

    def _get_azure_workspace(self) -> "Workspace":
        return self.provider().get_workspace()

    def _get_azure_target_id(self) -> str:
        return self.name()

    def _get_azure_provider_id(self) -> str:
        return self._azure_config()["provider_id"]


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
            "output_data_format": "microsoft.quantum-results.v2",
            "is_default": True,
        }
    
    def _basis_gates(self) -> List[str]:
        return QIR_BASIS_GATES

    def run(
        self,
        run_input: Union[QuantumCircuit, List[QuantumCircuit]] = [],
        shots: int = None, 
        **options,
    ) -> AzureQuantumJob:
        """Run on the backend.

        This method returns a
        :class:`~azure.quantum.qiskit.job.AzureQuantumJob` object
        that runs circuits.

        Args:
            run_input (QuantumCircuit or List[QuantumCircuit]): An individual or a
            list of one :class:`~qiskit.circuits.QuantumCircuit` to run on the backend.
            shots (int, optional): Number of shots, defaults to None.
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

        circuit = run_input
        if isinstance(run_input, list):
            # just in case they passed a list, we only support single-experiment jobs
            if len(run_input) != 1:
                raise NotImplementedError(
                    f"This backend only supports running a single circuit per job."
                )
            circuit = run_input[0]
            if not isinstance(circuit, QuantumCircuit):
                raise ValueError("Invalid input: expected a QuantumCircuit.")

        # config normalization
        input_params = self._get_input_params(options, shots=shots)
        
        shots_count = None

        if self._can_send_shots_input_param():
            shots_count = input_params.get(self.__class__._SHOTS_PARAM_NAME)

        job_name = options.pop("job_name", circuit.name)

        metadata = options.pop("metadata", self._prepare_job_metadata(circuit))

        input_data = self._translate_input(circuit, input_params)

        job = super()._run(job_name, input_data, input_params, metadata, **options)
        logger.info(
            f"Submitted job with id '{job.id()}' with shot count of {shots_count}:"
        )

        return job

    def _prepare_job_metadata(self, circuit: QuantumCircuit) -> Dict[str, str]:
        """Returns the metadata relative to the given circuits that will be attached to the Job"""
        return {
            "qiskit": str(True),
            "name": circuit.name,
            "num_qubits": circuit.num_qubits,
            "metadata": json.dumps(circuit.metadata),
        }


    def _get_qir_str(
        self, circuit: QuantumCircuit, target_profile: TargetProfile, **kwargs
    ) -> str:

        config = self.configuration()
        # Barriers aren't removed by transpilation and must be explicitly removed in the Qiskit to QIR translation.
        supports_barrier = "barrier" in config.basis_gates
        skip_transpilation = kwargs.pop("skip_transpilation", False)

        backend = QSharpBackend(
            qiskit_pass_options={"supports_barrier": supports_barrier},
            target_profile=target_profile,
            skip_transpilation=skip_transpilation,
            **kwargs,
        )

        qir_str = backend.qir(circuit)
        
        return qir_str


    def _translate_input(
        self, circuit: QuantumCircuit, input_params: Dict[str, Any]
    ) -> bytes:
        """Translates the input values to the QIR expected by the Backend."""
        logger.info(f"Using QIR as the job's payload format.")

        target_profile = self._get_target_profile(input_params)

        if logger.isEnabledFor(logging.DEBUG):
            qir = self._get_qir_str(circuit, target_profile, skip_transpilation=True)
            logger.debug(f"QIR:\n{qir}")

        # We'll transpile automatically to the supported gates in QIR unless explicitly skipped.
        skip_transpilation = input_params.pop("skipTranspile", False)

        qir_str = self._get_qir_str(
            circuit, target_profile, skip_transpilation=skip_transpilation
        )

        entry_points = ["ENTTRYPOINT_main"]

        if not skip_transpilation:
            # We'll only log the QIR again if we performed a transpilation.
            if logger.isEnabledFor(logging.DEBUG):
                qir = str(qir_str)
                logger.debug(f"QIR (Post-transpilation):\n{qir}")

        if "items" not in input_params:
            arguments = input_params.pop("arguments", [])
            input_params["items"] = [
                {"entryPoint": name, "arguments": arguments} for name in entry_points
            ]

        return qir_str.encode("utf-8")

    def _get_target_profile(self, input_params) -> TargetProfile:
        # Default to Adaptive_RI if not specified on the backend
        # this is really just a safeguard in case the backend doesn't have a default
        default_profile = self.options.get("target_profile", TargetProfile.Adaptive_RI)

        # If the user is using the old targetCapability parameter, we'll warn them
        # and use that value for now. This will be removed in the future.
        if "targetCapability" in input_params:
            warnings.warn(
                "The 'targetCapability' parameter is deprecated and will be ignored in the future. "
                "Please, use 'target_profile' parameter instead.",
                category=DeprecationWarning,
            )
            cap = input_params.pop("targetCapability")
            if cap == "AdaptiveExecution":
                default_profile = TargetProfile.Adaptive_RI
            else:
                default_profile = TargetProfile.Base
        # If the user specifies a target profile, use that.
        # Otherwise, use the profile we got from the backend/targetCapability.
        return input_params.pop("target_profile", default_profile)


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

    def run(
            self, 
            run_input: Union[QuantumCircuit, List[QuantumCircuit]] = [],
            shots: int = None,
            **options,
        ):
        """Submits the given circuit to run on an Azure Quantum backend.""" 
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
        if isinstance(circuit, QasmQobj) or isinstance(circuit, PulseQobj):
            from qiskit.assembler import disassemble

            circuits, run, _ = disassemble(circuit)
            circuit = circuits[0]
            if options.get("shots") is None:
                # Note that qiskit.assembler.disassemble() sets the default number of shots for QasmQobj and PulseQobj to 1024
                # unless the user specifies the backend.
                options["shots"] = run["shots"]

        # If not provided as options, the values of these parameters
        # are calculated from the circuit itself:
        job_name = options.pop("job_name", circuit.name)
        metadata = options.pop("metadata", self._prepare_job_metadata(circuit))

        input_params = self._get_input_params(options, shots=shots)

        input_data = self._translate_input(circuit)

        job = super()._run(job_name, input_data, input_params, metadata, **options)

        shots_count = None
        if self._can_send_shots_input_param():
            shots_count = input_params.get(self.__class__._SHOTS_PARAM_NAME)

        logger.info(
            f"Submitted job with id '{job.id()}' for circuit '{circuit.name}' with shot count of {shots_count}:"
        )
        logger.info(input_data)

        return job

def _get_shots_or_deprecated_count_input_param(
        param_name: str,
        shots: int = None, 
        count: int = None,
    ) -> Optional[int]:
    """
    This helper function checks if the deprecated 'count' option is specified.
    In earlier versions it was possible to pass this option to specify shots number for a job,
    but now we only check for it for compatibility reasons.  
    """

    final_shots = None

    if shots is not None:
        final_shots = shots
    
    elif count is not None:
        final_shots = count
        warnings.warn(
            "The 'count' parameter will be deprecated. "
            f"Please, use '{param_name}' parameter instead.",
            category=DeprecationWarning,
        )
    
    return final_shots