##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import abc
import cirq

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from azure.quantum import Job


class _CirqTargetMixin(abc.ABC):
    @abc.abstractstaticmethod
    def _translate_cirq_circuit(circuit):
        """Translate Cirq circuit to native provider format."""
        pass

    @classmethod
    def _translate_circuit(cls, circuit: Any):
        """Translate circuit into native provider format"""
        try:
            return cls._translate_cirq_circuit(circuit)
        except Exception as e:
            raise ValueError(
                f"Cannot translate circuit of type {circuit.__class__}: {e}")

    def submit(
        self,
        circuit: cirq.Circuit,
        name: str = "cirq-job",
        repetitions: int = None,
        **kwargs
    ) -> "Job":
        """Submit a Cirq quantum circuit

        :param circuit: Quantum circuit in IonQ JSON format
        :type circuit: Union[Dict[str, Any], CirqCircuit]
        :param name: Job name
        :type name: str
        :param repetitions: Number of shots, defaults to 
            provider default value
        :type repetitions: int
        :return: Azure Quantum job
        :rtype: Job
        """
        data = self._translate_circuit(circuit)
        return super().submit(
            circuit=data,
            name=name,
            num_shots=repetitions,
            **kwargs
        )
