##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from typing import TYPE_CHECKING

from azure.quantum.target import IonQ
from azure.quantum.plugins.cirq.targets.cirq_target import _CirqTargetMixin

if TYPE_CHECKING:
    from azure.quantum import Workspace


class IonQTarget(_CirqTargetMixin, IonQ):
    """Base class for interfacing with an IonQ backend in Azure Quantum"""
    target_name: str = "ionq.simulator"
    def __init__(
        self,
        workspace: "Workspace",
        name: str = None,
        input_data_format: str = "ionq.circuit.v1",
        output_data_format: str = "ionq.quantum-results.v1",
        provider_id: str = "IonQ",
        content_type: str = "application/json",
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
    def _translate_cirq_circuit(circuit):
        """Translate Cirq circuit to IonQ JSON. If dependencies \
    are not installed, throw error with installation instructions."""
        try:
            from cirq_ionq import Serializer

        except ImportError:
            raise ImportError(
                "Missing optional 'cirq_ionq' dependency. \
    To install run: pip install azure-quantum[cirq]")

        else:
            return Serializer().serialize(circuit).body


class IonQSimulatorTarget(IonQTarget):
    """Class for interfacing with an IonQ simulator target"""
    target_name = "ionq.simulator"


class IonQQPUTarget(IonQTarget):
    """Class for interfacing with an IonQ QPU target target"""
    target_name = "ionq.qpu"
