##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from collections import Counter
import uuid
import numpy as np

from azure.quantum import Job
from azure.quantum.workspace import Workspace
from azure.quantum.projectq.utils import (
    PROJECTQ_USER_AGENT, 
    HONEYWELL_PROVIDER, 
    HONEYWELL_INPUT_DATA_FORMAT, 
    HONEYWELL_OUTPUT_DATA_FORMAT
)
from azure.quantum.target.ionq import int_to_bitstring

try:
    # Using IBMBackend as HoneywellBackend to translate `projectq` circuit to QASM.
    from projectq.backends import IBMBackend as _HoneywellBackend
    from projectq.types import WeakQubitRef
except ImportError:
    raise ImportError(
    "Missing optional 'projectq' dependencies. \
To install run: pip install azure-quantum[projectq]"
)

import logging
logger = logging.getLogger(__name__)

__all__ = ["AzureHoneywellQPUBackend", "AzureHoneywellAPIValidatorBackend", "AzureHoneywellSimulatorBackend"]


class AzureHoneywellBackend(_HoneywellBackend):
    azure_quantum_backend_name: str = None

    def __init__(
        self, 
        workspace: Workspace, 
        use_hardware: bool=False,
        num_runs: int=100,
        verbose: bool=False,
        device: str="honeywell.hqs-lt-s1-sim",
        retrieve_execution: str=None
    ):
        """Base class for interfacing with a Honeywell backend in Azure Quantum

        :param use_hardware: Whether or not to use real Honeywell hardware or just a simulator. If False, the
            Honeywell simulator is used regardless of the value of ``device``. Defaults to False.
        :param num_runs: Number of times to run circuits. Defaults to 100.
        verbose: If True, print statistics after job results have been collected. Defaults to
            False.
        :param device: Device to run jobs on. Defaults to ``'honeywell.hqs-lt-s1-sim'``.
        :param retrieve_execution: An Honeywell API Job ID.  If provided, a job with this ID will be
            fetched. Defaults to None.
        """
        logger.info("Initializing HoneywellBackend for ProjectQ")

        workspace.append_user_agent(PROJECTQ_USER_AGENT)
        self._workspace = workspace

        if not use_hardware:
            device = "honeywell.hqs-lt-s1-sim"

        super().__init__(
            use_hardware=True, 
            num_runs=num_runs, 
            verbose=verbose,
            device=device,
            retrieve_execution=retrieve_execution
        )

    def submit_job(self, name=None, **kwargs) -> Job:
        """Submits the given circuit to run on an Honeywell target."""
        for measured_id in self._measured_ids:
            qb_loc = self.main_engine.mapper.current_mapping[measured_id]
            self.qasm += "\nmeasure q[{0}] -> c[{0}];".format(qb_loc)

        if not self.qasm:
            logger.debug("Cannot run circuit because it is empty.")
            return

        logger.info(f"Submitting new job for backend {self.device}")

        if name is None:
            random_suffix = str(uuid.uuid4())[:8]
            name = "projectq-honeywell-circuit-{}".format(random_suffix)

        # saving measured_ids in base class variable, self.reset will cleanup self._measured_ids
        # measured_ids is required for construct self._probabilities in self._run method.
        self.measured_ids = self._measured_ids[:]

        num_qubits = len(self._measured_ids)

        qasm = self.get_qasm()
        qasm = qasm.replace("u2(0,pi/2)", "h")
        input_data = f"OPENQASM 2.0;\ninclude \"qelib1.inc\";\nqreg q[{num_qubits}];\ncreg c[{num_qubits}];{qasm}\n"

        input_params = {
            "shots": self._num_runs
        }

        metadata = {
            "num_qubits": num_qubits
        }

        job = Job.from_input_data(
            workspace=self._workspace,
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

        logger.info(f"Submitted job with id '{job.id}' for circuit '{name}':")
        logger.info(input_data)

        # reset engine state
        self._reset()

        return job

    def _run(self):
        """
        Run a ProjectQ circuit and wait until it is done.
        """
        job = self.submit_job()
        if job:
            result = job.get_results()
            histogram = Counter(result["c"])
            num_shots = sum(histogram.values())
            self._probabilities = {int_to_bitstring(k, len(self.measured_ids), self.measured_ids): v/num_shots for k, v in histogram.items()}

            # Set a single measurement result
            bitstring = np.random.choice(list(self._probabilities.keys()), p=list(self._probabilities.values()))
            for qid in self.measured_ids:
                qubit_ref = WeakQubitRef(self.main_engine, qid)
                self.main_engine.set_measurement_result(qubit_ref, bitstring[qid])


class AzureHoneywellQPUBackend(AzureHoneywellBackend):
    backend_names = (
        "honeywell.hqs-lt-s1",
        "honeywell.hqs-lt-s2"
    )

    def __init__(
        self, 
        workspace: Workspace,
        num_runs=100, 
        verbose=False, 
        device="honeywell.hqs-lt-s1", 
        retrieve_execution=None
    ):
        """Base class for interfacing with an Honeywell QPU backend"""
        logger.info("Initializing HoneywellQPUBackend for ProjectQ")

        super().__init__(
            workspace=workspace,
            use_hardware=True, 
            num_runs=num_runs, 
            verbose=verbose, 
            device=device, 
            retrieve_execution=retrieve_execution
        )


class AzureHoneywellAPIValidatorBackend(AzureHoneywellBackend):
    backend_names = (
        "honeywell.hqs-lt-s1-apival",
        "honeywell.hqs-lt-s2-apival"
    )

    def __init__(
        self, 
        workspace: Workspace,
        num_runs=100, 
        verbose=False, 
        device="honeywell.hqs-lt-s1-apival", 
        retrieve_execution=None
    ):
        """Base class for interfacing with an Honeywell APIValidator backend"""
        logger.info("Initializing HoneywellAPIValidatorBackend for ProjectQ")

        super().__init__(
            workspace=workspace,
            use_hardware=False, 
            num_runs=num_runs, 
            verbose=verbose, 
            device=device, 
            retrieve_execution=retrieve_execution
        )


class AzureHoneywellSimulatorBackend(AzureHoneywellBackend):
    backend_names = (
        "honeywell.hqs-lt-s1-sim",
        "honeywell.hqs-lt-s2-sim"
    )

    def __init__(
        self, 
        workspace: Workspace,
        num_runs=100, 
        verbose=False, 
        device="honeywell.hqs-lt-s1-sim", 
        retrieve_execution=None
    ):
        """Base class for interfacing with an Honeywell Simulator backend"""
        logger.info("Initializing HoneywellSimulatorBackend for ProjectQ")

        super().__init__(
            workspace=workspace,
            use_hardware=False, 
            num_runs=num_runs, 
            verbose=verbose, 
            device=device, 
            retrieve_execution=retrieve_execution
        )
