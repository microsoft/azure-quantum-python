##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from typing import Any, Dict
from warnings import warn

from azure.quantum.target.target import (
    Target,
    _determine_shots_or_deprecated_num_shots,
)
from azure.quantum.job.job import Job
from azure.quantum.workspace import Workspace
from azure.quantum._client.models import CostEstimate, UsageEvent
from typing import Union


class Quantinuum(Target):
    """Quantinuum target."""
    target_names = (
        # Note: Target names on the same line are equivalent.
        "quantinuum.qpu.h1-1",
        "quantinuum.sim.h1-1sc",
        "quantinuum.sim.h1-1e",
        "quantinuum.qpu.h2-1",
        "quantinuum.sim.h2-1sc",
        "quantinuum.sim.h2-1e",
    )

    _SHOTS_PARAM_NAME = "count"

    def __init__(
        self,
        workspace: Workspace,
        name: str = "quantinuum.sim.h1-1sc",
        input_data_format: str = "honeywell.openqasm.v1",
        output_data_format: str = "honeywell.quantum-results.v1",
        capability: str = "AdaptiveExecution",
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
            capability=capability,
            provider_id=provider_id,
            content_type=content_type,
            encoding=encoding,
            **kwargs
        )

    def submit(
        self,
        circuit: str = None,
        name: str = "quantinuum-job",
        shots: int = None,
        input_params: Dict[str, Any] = None,
        **kwargs
    ) -> Job:
        """Submit a Quantinuum program (OpenQASM 2.0 format)

        :param circuit: Quantum circuit in Quantinuum OpenQASM 2.0 format
        :type circuit: str
        :param name: Job name
        :type name: str
        :param shots: Number of shots, defaults to None
        :type shots: int
        :param input_params: Optional input params dict
        :type input_params: Dict[str, Any]
        :return: Azure Quantum job
        :rtype: Job
        """
        input_data = kwargs.pop("input_data", circuit)
        if input_data is None:
            raise ValueError(
                "Either the `circuit` parameter or the `input_data` parameter must have a value."
            )
        if input_params is None:
            input_params = {}

        num_shots = kwargs.pop("num_shots", None)

        shots = _determine_shots_or_deprecated_num_shots(
            shots=shots,
            num_shots=num_shots,
        )

        return super().submit(
            input_data=input_data,
            name=name,
            shots=shots,
            input_params=input_params,
            **kwargs
        )

    def estimate_cost(
        self,
        circuit: Union[str, Any] = None,
        num_shots: int = None,
        N_1q: int = None,
        N_2q: int = None,
        N_m: int = None,
        shots: int = None,
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
        :type num_shots: int
        :param N_1q: Number of one-qubit gates, if not specified,
            this is estimated from the circuit
        :type N_1q: int
        :param N_2q: Number of two-qubit gates, if not specified,
            this is estimated from the circuit
        :type N_2q: int
        :param N_m: Number of measurement operations, if not specified,
            this is estimated from the circuit
        :type N_m: int
        :param shots: Number of shots for which to estimate costs
        :type shots: int
        :raises ImportError: If N_1q, N_2q and N_m are not specified,
            this will require a qiskit installation.
        """

        if num_shots is None and shots is None:
             raise ValueError("The 'shots' parameter has to be specified")

        if num_shots is not None:
            warn(
                "The 'num_shots' parameter will be deprecated. Please, use 'shots' parameter instead.",
                category=DeprecationWarning,
            )
            shots = num_shots

        # If we use passthrough, else assume QIR
        if (isinstance(circuit, str)):
            if circuit is not None and (N_1q is None or N_2q is None or N_m is None):
                try:
                    from qiskit.qasm2 import loads
                    from qiskit.converters.circuit_to_dag import circuit_to_dag

                except ImportError:
                    raise ImportError(
                        "Missing dependency qiskit. Please run `pip install azure-quantum[qiskit]` " \
    "to estimate the circuit cost. Alternatively, specify the number of one-qubit and two-qubit " \
    "gates in the method input arguments.")

                else:
                    from qiskit.dagcircuit.dagnode import DAGOpNode
                    circuit_obj = loads(string=circuit)
                    dag = circuit_to_dag(circuit=circuit_obj)
                    N_1q, N_2q, N_m = 0, 0, 0
                    for node in dag._multi_graph.nodes():
                        if isinstance(node, DAGOpNode):
                            if node.op.name in ["measure", "reset"]:
                                N_m += 1
                            elif node.op.num_qubits == 1:
                                N_1q += 1
                            else:
                                N_2q += 1
        else:
            N_1q, N_2q, N_m = Target._calculate_qir_module_gate_stats(circuit)
            

        import re
        is_emulator_regex = re.compile("^.*(-sim|-[0-9]*e)$")
        is_syntax_checker_regex = re.compile("^.*(-apival|-[0-9]*sc)$")

        if is_emulator_regex.match(self.name):
            currency_code = "EHQC"
        else:
            currency_code = "HQC"

        if is_syntax_checker_regex.match(self.name):
            HQC = 0.0
        else:
            HQC = 5 + shots * (N_1q + 10 * N_2q + 5 * N_m) / 5000

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
