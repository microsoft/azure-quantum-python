##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import io
from typing import Any, Dict

from azure.quantum.target.target import Target
from azure.quantum.job.job import Job
from azure.quantum.workspace import Workspace


class Honeywell(Target):
    """Honeywell target."""
    target_names = (
        "honeywell.hqs-lt-s1",
        "honeywell.hqs-lt-s1-apival",
        "honeywell.hqs-lt-s1-sim",
    )

    # Get all one-qubit, two-qubit gates and measurement operations
    GATES_1Q = [
        "x",
        "y",
        "z",
        "rx",
        "ry",
        "rz",
        "h",
        "s",
        "sdg",
        "t",
        "tdg",
        "v",
        "vdg",
    ]

    GATES_MULTI = [
        "cx",
        "ccx",
        "cz",
        "zz",
    ]

    GATES_M = [
        "measure",
        "reset"
    ]

    def __init__(
        self,
        workspace: Workspace,
        name: str = "honeywell.hqs-lt-s1-apival",
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
    def _encode_input_data(data: str) -> bytes:
        stream = io.BytesIO()
        stream.write(data.encode())
        return stream.getvalue()

    def submit(
        self,
        circuit: str,
        name: str = "honeywell-job",
        num_shots: int = None,
        input_params: Dict[str, Any] = None,
        **kwargs
    ) -> Job:
        """Submit a Honeywell program (QASM format)

        :param circuit: Quantum circuit in Honeywell QASM format
        :type circuit: str
        :param name: Job name
        :type name: str
        :param num_shots: Number of shots, defaults to None
        :type num_shots: int
        :param input_params: Optional input params dict
        :type input_params: Dict[str, Any]
        :return: Azure Quantum job
        :rtype: Job
        """
        if input_params is None:
            input_params = {}
        if num_shots is not None:
            input_params = input_params.copy()
            input_params["count"] = num_shots

        return super().submit(
            input_data=circuit,
            name=name,
            input_params=input_params,
            **kwargs
        )
    
    def estimate_price(
        self,
        circuit: str = None,
        num_shots: int = None,
        N_1q: int = None,
        N_2q: int = None,
        N_m: int  = None
    ):
        """Estimate the price in HQC for a given circuit.
        Optionally, you can provide the number of gate and measurement operations
        manually.
        The actual price charged by the provider may differ from this estimation.

        For the most current pricing details, see
        https://docs.microsoft.com/en-us/azure/quantum/provider-honeywell#honeywell-system-model-h1
        Or find your workspace and view pricing options in the "Provider" tab
        of your workspace: http://aka.ms/aq/myworkspaces

        :param circuit: Quantum circuit in QASM format
        :type circuit: str
        :param num_shots: Number of shots for which to estimate costs
        :type num_shots: int, optional
        :param N_1q: Number of one-qubit gates, if not specified, 
            this is estimated from the circuit
        :type N_1q: int, optional
        :param N_2q: Number of two-qubit gates, if not specified, 
            this is estimated from the circuit
        :type N_2q: int, optional
        :param N_m: Number of measurement operations, if not specified, 
            this is estimated from the circuit
        :type N_m: int, optional
        :raises ImportError: If N_1q, N_2q and N_m are not specified,
            this will require a qiskit installation.
        """
        if "apival" in self.name:
            return 0.0

        if circuit is not None and (N_1q is None or N_2q is None or N_m is None):
            try:
                from qiskit.circuit.quantumcircuit import Qasm
                from qiskit.converters import ast_to_dag

            except ImportError:
                raise ImportError(
                    "Missing dependency qiskit. Please run `pip install azure-quantum[qiskit]` " \
"to estimate the circuit cost. Alternatively, specify the number of one-qubit and two-qubit " \
"gates in the method input arguments.")

            else:
                qasm = Qasm(data=circuit)
                ast = qasm.parse()
                dag = ast_to_dag(ast)
                ops = dag.count_ops()
                N_1q = sum([value for key, value in ops.items() if key in self.GATES_1Q])
                N_2q = sum([value for key, value in ops.items() if key in self.GATES_MULTI])
                N_m = sum([value for key, value in ops.items() if key in self.GATES_M])

        HQC = 5 + num_shots * (N_1q + 10 * N_2q + 5 * N_m) / 5000

        return HQC
