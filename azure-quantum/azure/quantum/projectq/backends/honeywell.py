##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import uuid

from azure.quantum import __version__
from azure.quantum.projectq.job import (
    AzureQuantumJob, 
    HONEYWELL_PROVIDER, 
    HONEYWELL_INPUT_DATA_FORMAT, 
    HONEYWELL_OUTPUT_DATA_FORMAT
)

try:
    # Using IBMBackend as HoneywellBackend to translate `projectq` circuit to QASM.
    from projectq.backends import IBMBackend as _HoneywellBackend
    from projectq.cengines import BasicMapperEngine
    import projectq.setups.restrictedgateset
    from projectq.ops import (
        X,
        Y,
        Z,
        Rx,
        Ry,
        Rz,
        H,
        CX,
        CZ,
        S,
        Sdag,
        T,
        Tdag,
        Toffoli,
    )
except ImportError:
    raise ImportError(
    "Missing optional 'projectq' dependencies. \
To install run: pip install azure-quantum[projectq]"
)

import logging
logger = logging.getLogger(__name__)

__all__ = ["HoneywellQPUBackend", "HoneywellAPIValidatorBackend", "HoneywellSimulatorBackend"]


class HoneywellBackend(_HoneywellBackend):
    azure_quantum_backend_name: str = None

    def __init__(
        self, 
        use_hardware=False, 
        num_runs=100, 
        verbose=False, 
        device="honeywell.hqs-lt-s1-apival", 
        retrieve_execution=None
    ):
        """Base class for interfacing with an Honeywell backend in Azure Quantum"""
        logger.info("Initializing HoneywellBackend for ProjectQ")

        super().__init__(
            use_hardware=use_hardware, 
            num_runs=num_runs, 
            verbose=verbose, 
            retrieve_execution=retrieve_execution
        )

        # Overriding IBMBackend device name with Honeywell device name.
        self.device = device

    def get_engine_list(self):
        """Return the default list of compiler engine for the Honeywell platform."""
        mapper = BasicMapperEngine()
        num_qubits = 10

        mapping = {}
        for i in range(num_qubits):
            mapping[i] = i

        mapper.current_mapping = mapping

        engine_list = projectq.setups.restrictedgateset.get_engine_list(
            one_qubit_gates=(X, Y, Z, Rx, Ry, Rz, H, S, Sdag, T, Tdag),
            two_qubit_gates=(CX, CZ),
            other_gates=(Toffoli,)
        )

        return engine_list + [mapper]

    def submit_job(self, name=None, **kwargs):
        """Submits the given circuit to run on an Honeywell target."""
        logger.info(f"Submitting new job for backend {self.device}")

        if name is None:
            random_suffix = str(uuid.uuid4())[:8]
            name = "projectq-honeywell-circuit-{}".format(random_suffix)

        qubit_mapping = self.main_engine.mapper.current_mapping
        num_qubits = len(qubit_mapping.keys())

        input_data = self.get_qasm()

        input_params = {
            "shots": self._num_runs
        }

        metadata = {
            "num_qubits": num_qubits
        }

        job = AzureQuantumJob(
            backend=self,
            name=name,
            target=self.device,
            input_data=input_data,
            blob_name="inputData",
            content_type="application/qasm",
            job_id=self._retrieve_execution,
            provider_id=HONEYWELL_PROVIDER,
            input_data_format=HONEYWELL_INPUT_DATA_FORMAT,
            output_data_format=HONEYWELL_OUTPUT_DATA_FORMAT,
            input_params=input_params,
            metadata=metadata,
            **kwargs
        ) 

        logger.info(f"Submitted job with id '{job.id()}' for circuit '{name}':")
        logger.info(input_data)

        return job

    def _run(self):
        """
        Overriding Projectq run method with empty function.
        This disables circuit execution using default ProjectQ logic. Use engine.run() to submit job to Azure Quantum.
        """
        pass


class HoneywellQPUBackend(HoneywellBackend):
    backend_names = (
        "honeywell.hqs-lt-s1",
        "honeywell.hqs-lt-s2"
    )

    def __init__(
        self, 
        num_runs=100, 
        verbose=False, 
        device="honeywell.hqs-lt-s1", 
        retrieve_execution=None
    ):
        """Base class for interfacing with an Honeywell QPU backend"""
        logger.info("Initializing HoneywellQPUBackend for ProjectQ")

        super().__init__(
            use_hardware=True, 
            num_runs=num_runs, 
            verbose=verbose, 
            device=device, 
            retrieve_execution=retrieve_execution
        )


class HoneywellAPIValidatorBackend(HoneywellBackend):
    backend_names = (
        "honeywell.hqs-lt-s1-apival",
        "honeywell.hqs-lt-s2-apival"
    )

    def __init__(
        self, 
        num_runs=100, 
        verbose=False, 
        device="honeywell.hqs-lt-s1-apival", 
        retrieve_execution=None
    ):
        """Base class for interfacing with an Honeywell APIValidator backend"""
        logger.info("Initializing HoneywellAPIValidatorBackend for ProjectQ")

        super().__init__(
            use_hardware=False, 
            num_runs=num_runs, 
            verbose=verbose, 
            device=device, 
            retrieve_execution=retrieve_execution
        )


class HoneywellSimulatorBackend(HoneywellBackend):
    backend_names = (
        "honeywell.hqs-lt-s1-sim",
        "honeywell.hqs-lt-s2-sim"
    )

    def __init__(
        self, 
        num_runs=100, 
        verbose=False, 
        device="honeywell.hqs-lt-s1-sim", 
        retrieve_execution=None
    ):
        """Base class for interfacing with an Honeywell Simulator backend"""
        logger.info("Initializing HoneywellSimulatorBackend for ProjectQ")

        super().__init__(
            use_hardware=False, 
            num_runs=num_runs, 
            verbose=verbose, 
            device=device, 
            retrieve_execution=retrieve_execution
        )
