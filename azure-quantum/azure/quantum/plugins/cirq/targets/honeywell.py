##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from typing import TYPE_CHECKING
from azure.quantum.target import Honeywell
from azure.quantum.plugins.cirq.targets.cirq_target import _CirqTargetMixin

if TYPE_CHECKING:
    from azure.quantum import Workspace

class HoneywellTarget(_CirqTargetMixin, Honeywell):
    """Base class for interfacing with an Honeywell backend in Azure Quantum"""
    target_name: str = None

    def __init__(
        self,
        workspace: "Workspace",
        name: str = None,
        input_data_format: str = "honeywell.openqasm.v1",
        output_data_format: str = "honeywell.quantum-results.v1",
        provider_id: str = "honeywell",
        content_type: str = "application/qasm",
        encoding: str = "",
        **kwargs
    ):
        super().__init__(
            workspace=workspace,
            name=name or self.target_name,
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


class HoneywellAPIValidatorTarget(HoneywellTarget):
    """Class for interfacing with a Honeywell API validator target"""
    target_name = "honeywell.hqs-lt-s1-apival"


class HoneywellSimulatorTarget(HoneywellTarget):
    """Class for interfacing with a Honeywell Simulator target"""
    target_name = "honeywell.hqs-lt-s1-sim"


class HoneywellQPUTarget(HoneywellTarget):
    """Class for interfacing with a Honeywell QPU target"""
    target_name = "honeywell.hqs-lt-s1"
