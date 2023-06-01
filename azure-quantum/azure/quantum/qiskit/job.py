##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from collections import defaultdict
from typing import Any, Dict, List, Union
import numpy as np

try:
    from qiskit.providers import JobV1, JobStatus
    from qiskit.result import Result
except ImportError:
    raise ImportError(
        "Missing optional 'qiskit' dependencies. \
To install run: pip install azure-quantum[qiskit]"
    )

import ast
import json
import re
from azure.quantum import Job
from azure.quantum.qiskit.results.resource_estimator import make_estimator_result

import logging
logger = logging.getLogger(__name__)

AzureJobStatusMap = {
    "Succeeded": JobStatus.DONE,
    "Waiting": JobStatus.QUEUED,
    "Executing": JobStatus.RUNNING,
    "Failed": JobStatus.ERROR,
    "Cancelled": JobStatus.CANCELLED,
    "Finishing": JobStatus.RUNNING
}

# Constants for output data format:
MICROSOFT_OUTPUT_DATA_FORMAT = "microsoft.quantum-results.v1"
MICROSOFT_OUTPUT_DATA_FORMAT_V2 = "microsoft.quantum-results.v2"
IONQ_OUTPUT_DATA_FORMAT = "ionq.quantum-results.v1"
QUANTINUUM_OUTPUT_DATA_FORMAT = "honeywell.quantum-results.v1"
RESOURCE_ESTIMATOR_OUTPUT_DATA_FORMAT = "microsoft.resource-estimates.v1"

class AzureQuantumJob(JobV1):
    def __init__(
        self,
        backend,
        azure_job=None,
        **kwargs
    ) -> None:
        """
            A Job running on Azure Quantum
        """
        if azure_job is None:
            azure_job = Job.from_input_data(
                workspace=backend.provider().get_workspace(),
                session_id=backend.get_latest_session_id(),
                **kwargs
            )

        self._azure_job = azure_job
        self._workspace = backend.provider().get_workspace()

        super().__init__(backend, self._azure_job.id, **kwargs)

    def job_id(self):
        """ This job's id."""
        return self._azure_job.id

    def id(self):
        """ This job's id."""
        return self._azure_job.id

    def refresh(self):
        """ Refreshes the job metadata from the server."""
        return self._azure_job.refresh()

    def submit(self):
        """ Submits the job for execution. """
        self._azure_job.submit()
        return

    def result(self, timeout=None, sampler_seed=None):
        """Return the results of the job."""
        self._azure_job.wait_until_completed(timeout_secs=timeout)

        success = self._azure_job.details.status == "Succeeded"
        results = self._format_results(sampler_seed=sampler_seed)

        result_dict = {
            "results" : results if isinstance(results, list) else [results],
            "job_id" : self._azure_job.details.id,
            "backend_name" : self._backend.name(),
            "backend_version" : self._backend.version,
            "qobj_id" : self._azure_job.details.name,
            "success" : success,
            "error_data" : None if self._azure_job.details.error_data is None else self._azure_job.details.error_data.as_dict()
        }

        if self._azure_job.details.output_data_format == RESOURCE_ESTIMATOR_OUTPUT_DATA_FORMAT:
            return make_estimator_result(result_dict)
        else:
            return Result.from_dict(result_dict)

    def cancel(self):
        """Attempt to cancel the job."""
        self._workspace.cancel_job(self._azure_job)

    def status(self):
        """Return the status of the job, among the values of ``JobStatus``."""
        self._azure_job.refresh()
        status = AzureJobStatusMap[self._azure_job.details.status]
        return status

    def queue_position(self):
        """Return the position of the job in the queue. Currently not supported."""
        return None

    def _shots_count(self):
        # Some providers use 'count', some other 'shots', give preference to 'count':
        input_params = self._azure_job.details.input_params
        options = self.backend().options
        shots = \
            input_params["count"] if "count" in input_params else \
            input_params["shots"] if "shots" in input_params else \
            options.get("count") if "count" in vars(options) else \
            options.get("shots")

        return shots

    def _format_results(self, sampler_seed=None) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """ Populates the results datastructures in a format that is compatible with qiskit libraries. """

        if (self._azure_job.details.output_data_format == MICROSOFT_OUTPUT_DATA_FORMAT_V2):
            return self._format_microsoft_v2_results()

        success = self._azure_job.details.status == "Succeeded"

        job_result = {
            "data": {},
            "success": success,
            "header": {},
        }

        if success:
            if (self._azure_job.details.output_data_format == MICROSOFT_OUTPUT_DATA_FORMAT):
                job_result["data"] = self._format_microsoft_results(sampler_seed=sampler_seed)
                
            elif (self._azure_job.details.output_data_format == IONQ_OUTPUT_DATA_FORMAT):
                job_result["data"] = self._format_ionq_results(sampler_seed=sampler_seed)

            elif (self._azure_job.details.output_data_format == QUANTINUUM_OUTPUT_DATA_FORMAT):
                job_result["data"] = self._format_quantinuum_results()

            else:
                job_result["data"] = self._format_unknown_results()

        job_result["header"] = self._azure_job.details.metadata
        if "metadata" in job_result["header"]:
            job_result["header"]["metadata"] = json.loads(job_result["header"]["metadata"])

        job_result["shots"] = self._shots_count()
        return job_result

    def _draw_random_sample(self, sampler_seed, probabilities, shots):
        _norm = sum(probabilities.values())
        if _norm != 1:
            if np.isclose(_norm, 1.0, rtol=1e-4):
                probabilities = {k: v/_norm for k, v in probabilities.items()}
            else:
                raise ValueError(f"Probabilities do not add up to 1: {probabilities}")
        if not sampler_seed:
            import hashlib
            id = self.job_id()
            sampler_seed = int(hashlib.sha256(id.encode('utf-8')).hexdigest(), 16) % (2**32 - 1)
        rand = np.random.RandomState(sampler_seed)
        rand_values = rand.choice(list(probabilities.keys()), shots, p=list(probabilities.values()))
        return dict(zip(*np.unique(rand_values, return_counts=True)))

    @staticmethod
    def _to_bitstring(k, num_qubits, meas_map):
        # flip bitstring to convert to little Endian
        bitstring = format(int(k), f"0{num_qubits}b")[::-1]
        # flip bitstring to convert back to big Endian
        return "".join([bitstring[n] for n in meas_map])[::-1]

    def _format_ionq_results(self, sampler_seed=None):
        """ Translate IonQ's histogram data into a format that can be consumed by qiskit libraries. """
        az_result = self._azure_job.get_results()
        shots = self._shots_count()

        if "num_qubits" not in self._azure_job.details.metadata:
            raise ValueError(f"Job with ID {self.id()} does not have the required metadata (num_qubits) to format IonQ results.")

        meas_map = json.loads(self._azure_job.details.metadata.get("meas_map")) if "meas_map" in self._azure_job.details.metadata else None
        num_qubits = self._azure_job.details.metadata.get("num_qubits")

        if not 'histogram' in az_result:
            raise "Histogram missing from IonQ Job results"

        counts = defaultdict(int)
        probabilities = defaultdict(int)
        for key, value in az_result['histogram'].items():
            bitstring = self._to_bitstring(key, num_qubits, meas_map) if meas_map else key
            probabilities[bitstring] += value

        if self.backend().configuration().simulator:
            counts = self._draw_random_sample(sampler_seed, probabilities, shots)
        else:
            counts = {bitstring: np.round(shots * value) for bitstring, value in probabilities.items()}

        return {"counts": counts, "probabilities": probabilities}

    @staticmethod
    def _qir_to_qiskit_bitstring(obj):
        """Convert the data structure from Azure into the "schema" used by Qiskit """
        if isinstance(obj, str) and not re.match(r"[\d\s]+$", obj):
            obj = ast.literal_eval(obj)

        if isinstance(obj, tuple):
            # the outermost implied container is a tuple, and each item is
            # associated with a classical register. Azure and Qiskit order the
            # registers in opposite directions, so reverse here to match.
            return " ".join([AzureQuantumJob._qir_to_qiskit_bitstring(term) for term in reversed(obj)])
        elif isinstance(obj, list):
            # a list is for an individual classical register
            return "".join([str(bit) for bit in obj])
        else:
            return str(obj)

    def _format_microsoft_results(self, sampler_seed=None):
        """ Translate Microsoft's job results histogram into a format that can be consumed by qiskit libraries. """
        az_result = self._azure_job.get_results()
        shots = self._shots_count()

        if not 'Histogram' in az_result:
            raise "Histogram missing from Job results"

        histogram = az_result['Histogram']
        counts = {}
        probabilities = {}
        # The Histogram serialization is odd entries are key and even entries values
        # Make sure we have even entries
        if (len(histogram) % 2) == 0:
            items = range(0, len(histogram), 2)
            for i in items:
                bitstring = AzureQuantumJob._qir_to_qiskit_bitstring(histogram[i])

                value = histogram[i + 1]
                probabilities[bitstring] = value
        else:
            raise "Invalid number of items in Job results' histogram."

        if self.backend().configuration().simulator:
            counts = self._draw_random_sample(sampler_seed, probabilities, shots)
        else:
            counts = {bitstring: np.round(shots * value) for bitstring, value in probabilities.items()}

        return {"counts": counts, "probabilities": probabilities}
    
    def _format_quantinuum_results(self):
        """ Translate Quantinuum's histogram data into a format that can be consumed by qiskit libraries. """
        az_result = self._azure_job.get_results()
        all_bitstrings = [
            bitstrings for classical_register, bitstrings 
            in az_result.items() if classical_register != "access_token"
        ]
        counts = {}
        combined_bitstrings = ["".join(bitstrings) for bitstrings in zip(*all_bitstrings)]
        shots = len(combined_bitstrings)

        for bitstring in set(combined_bitstrings):
            counts[bitstring] = combined_bitstrings.count(bitstring)

        histogram = {bitstring: count/shots for bitstring, count in counts.items()}

        return {"counts": counts, "probabilities": histogram}

    def _format_unknown_results(self):
        """ This method is called to format Job results data when the job output is in an unknown format."""
        az_result = self._azure_job.get_results()
        return az_result

    def _translate_microsoft_v2_results(self):
        """ Translate Microsoft's batching job results histograms into a format that can be consumed by qiskit libraries. """
        az_result = self._azure_job.get_results()

        if not "DataFormat" in az_result:
            raise ValueError("DataFormat missing from Job results")

        if not "Results" in az_result:
            raise ValueError("Results missing from Job results")

        histograms = []
        results = az_result["Results"]
        for circuit_results in results:
            counts = {}
            probabilities = {}

            if not "TotalCount" in circuit_results:
                raise ValueError("TotalCount missing from Job results")

            total_count = circuit_results["TotalCount"]

            if total_count <= 0:
                raise ValueError("TotalCount must be a positive non-zero integer")

            if not "Histogram" in circuit_results:
                raise ValueError("Histogram missing from Job results")
        
            histogram = circuit_results["Histogram"]
            for result in histogram:
                if not "Display" in result:
                    raise ValueError("Dispaly missing from histogram result")

                if not "Count" in result:
                    raise ValueError("Count missing from histogram result")

                bitstring = AzureQuantumJob._qir_to_qiskit_bitstring(result["Display"])
                count = result["Count"]
                probability = count / total_count
                counts[bitstring] = count
                probabilities[bitstring] = probability
            histograms.append((total_count, {"counts": counts, "probabilities": probabilities}))
        return histograms

    def _get_entry_point_names(self):
        input_params = self._azure_job.details.input_params
        # All V2 output is a list of entry points
        entry_points = input_params["items"]
        entry_point_names = []
        for entry_point in entry_points:
            if not "entryPoint" in entry_point:
                raise ValueError("Entry point input_param is missing an 'entryPoint' field")
            entry_point_names.append(entry_point["entryPoint"])
        return entry_point_names if len(entry_point_names) > 0 else ["main"]

    def _format_microsoft_v2_results(self) -> List[Dict[str, Any]]:
        success = self._azure_job.details.status == "Succeeded"

        if not success:
            return [{
                "data": {},
                "success": False,
                "header": {},
                "shots": 0,
            }]
        
        entry_point_names = self._get_entry_point_names()

        results = self._translate_microsoft_v2_results()
        
        if len(results) != len(entry_point_names):
            raise ValueError("The number of experiment results does not match the number of experiment names")
        
        status = self.status()

        return [{
            "data": result,
            "success": success,
            "shots": total_count,
            "name": name,
            "status": status,
            "header": {
                "name": name
            }
        } for name, (total_count, result) in zip(entry_point_names, results)]
