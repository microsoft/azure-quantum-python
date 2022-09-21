##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import io
from typing import Any, Dict

from azure.quantum.target.target import Target
from azure.quantum.job.job import Job
from azure.quantum.workspace import Workspace
from azure.quantum._client.models import CostEstimate, UsageEvent


class Quantinuum(Target):
    """Quantinuum (formerly Honeywell) target."""
    target_names = (
        "quantinuum.hqs-lt-s1",
        "quantinuum.hqs-lt-s1-apival",
        "quantinuum.hqs-lt-s1-sim",
        "quantinuum.hqs-lt-s2",
        "quantinuum.hqs-lt-s2-apival",
        "quantinuum.hqs-lt-s2-sim",
        "quantinuum.qpu.h1-1",
        "quantinuum.sim.h1-1sc",
        "quantinuum.sim.h1-1e"
        "quantinuum.qpu.h1-2",
        "quantinuum.sim.h1-2sc",
        "quantinuum.sim.h1-2e"
    )

    def __init__(
        self,
        workspace: Workspace,
        name: str = "quantinuum.sim.h1-1sc",
        input_data_format: str = "honeywell.openqasm.v1",
        output_data_format: str = "honeywell.quantum-results.v1",
        provider_id: str = "quantinuum",
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
        name: str = "quantinuum-job",
        num_shots: int = None,
        input_params: Dict[str, Any] = None,
        **kwargs
    ) -> Job:
        """Submit a Quantinuum (formerly Honeywell) program (OpenQASM 2.0 format)

        :param circuit: Quantum circuit in Quantinuum OpenQASM 2.0 format
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

    def estimate_cost(
        self,
        circuit: str = None,
        num_shots: int = None,
        N_1q: int = None,
        N_2q: int = None,
        N_m: int = None
    ) -> CostEstimate:
        """Estimate the cost in HQC for a given circuit.
        Optionally, you can provide the number of gate and measurement operations
        manually.
        The actual price charged by the provider may differ from this estimation.

        For the most current pricing details, see
        https://aka.ms/AQ/Quantinuum/Documentation
        Or find your workspace and view pricing options in the "Provider" tab
        of your workspace: https://aka.ms/aq/myworkspaces

        :param circuit: Quantum circuit in OpenQASM 2.0 format
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
                from qiskit.dagcircuit.dagnode import DAGOpNode
                qasm = Qasm(data=circuit)
                ast = qasm.parse()
                dag = ast_to_dag(ast)
                N_1q, N_2q, N_m = 0, 0, 0
                for node in dag._multi_graph.nodes():
                    if isinstance(node, DAGOpNode):
                        if node.op.name in ["measure", "reset"]:
                            N_m += 1
                        elif node.op.num_qubits == 1:
                            N_1q += 1
                        else:
                            N_2q += 1

        if "-sim" in self.name or "sim.h1-1e" in self.name or "sim.h1-2e" in self.name:
            currency_code = "EHQC"
        else:
            currency_code = "HQC"

        if "apival" in self.name or "sc" in self.name:
            HQC = 0.0
        else:
            HQC = 5 + num_shots * (N_1q + 10 * N_2q + 5 * N_m) / 5000

        return CostEstimate(
            events=[
                UsageEvent(
                    dimension_id="gates1q",
                    dimension_name="1Q Gates",
                    measure_unit="1q gates",
                    amount_billed=0.0,
                    amount_consumed=N_1q,
                    unit_price=0.0
                ),
                UsageEvent(
                    dimension_id="gates2q",
                    dimension_name="2Q Gates",
                    measure_unit="2q gates",
                    amount_billed=0.0,
                    amount_consumed=N_2q,
                    unit_price=0.0
                ),
                UsageEvent(
                    dimension_id="measops",
                    dimension_name="Measurement operations",
                    measure_unit="measurement operations",
                    amount_billed=0.0,
                    amount_consumed=N_m,
                    unit_price=0.0
                )
            ],
            currency_code=currency_code,
            estimated_total=HQC
        )
