##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import numpy as np

from typing import TYPE_CHECKING, Any, Dict

from azure.quantum.target import Honeywell
from azure.quantum.plugins.cirq.targets.target import Target as CirqTarget
from azure.quantum.plugins.cirq.job import Job as CirqJob

if TYPE_CHECKING:
    import cirq
    from azure.quantum import Workspace
    from azure.quantum import Job as AzureJob


class HoneywellTarget(Honeywell, CirqTarget):
    """Base class for interfacing with an Honeywell backend in Azure Quantum"""

    def __init__(
        self,
        workspace: "Workspace",
        name: str,
        input_data_format: str = "honeywell.openqasm.v1",
        output_data_format: str = "honeywell.quantum-results.v1",
        provider_id: str = "honeywell",
        content_type: str = "application/qasm",
        encoding: str = "",
        **kwargs
    ):
        super().__init__(
            workspace=workspace,
            name=name,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            provider_id=provider_id,
            content_type=content_type,
            encoding=encoding,
            **kwargs
        )

    @staticmethod
    def _translate_cirq_circuit(circuit) -> str:
        """Translate Cirq circuit to Honeywell QASM."""
        return circuit.to_qasm()
    
    @staticmethod
    def _to_cirq_result(result: Dict[str, Any], param_resolver, **kwargs):
        from cirq import Result
        measurements = {
            key.lstrip("m_"): np.array([[int(_v)] for _v in value])
            for key, value in result.items()
            if key.startswith("m_")
        }
        return Result(params=param_resolver, measurements=measurements)
    
    def _to_cirq_job(self, azure_job: "AzureJob", program: "cirq.Circuit" = None):
        """Convert Azure job to Cirq job"""
        if program is None:
            # Download QASM and convert to Cirq circuit
            from cirq.contrib.qasm_import import circuit_from_qasm
            uri = azure_job.details.input_data_uri
            qasm = azure_job.download_data(uri).decode("utf8")
            program = circuit_from_qasm(qasm)
        return CirqJob(azure_job=azure_job, program=program)

    def submit(
        self,
        program: "cirq.Circuit",
        name: str = "cirq-job",
        repetitions: int = 500,
        **kwargs
    ) -> "CirqJob":
        """Submit a Cirq quantum circuit

        :param program: Quantum program
        :type program: cirq.Circuit
        :param name: Job name
        :type name: str
        :param repetitions: Number of shots, defaults to 
            provider default value
        :type repetitions: int
        :return: Azure Quantum job
        :rtype: Job
        """
        serialized_program = self._translate_circuit(program)
        metadata = {
            "qubits": len(program.all_qubits()),
            "repetitions": repetitions
        }
        # Override metadata with value from kwargs
        metadata.update(kwargs.get("metadata", {}))
        azure_job = super().submit(
            circuit=serialized_program,
            name=name,
            num_shots=repetitions,
            metadata=metadata,
            **kwargs
        )
        return self._to_cirq_job(azure_job=azure_job, program=program)
