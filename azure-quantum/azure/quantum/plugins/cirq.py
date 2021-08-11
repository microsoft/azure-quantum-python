##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
def _is_cirq_circuit(circuit):
    try:
        from cirq.circuits import Circuit
        return isinstance(circuit, Circuit)
    except ImportError:
        return False

def translate_ionq_circuit(circuit):
    """Translate Cirq circuit to IonQ JSON. If dependencies \
are not installed, throw error with installation instructions."""
    try:
        from cirq_ionq import Serializer

    except ImportError:
        raise ImportError(
            "Missing optional 'cirq' dependencies. \
To install run: pip install azure-quantum[cirq]")

    else:
        return Serializer().serialize(circuit).body

__all__ = ["_is_cirq_circuit", "translate_ionq_circuit"]
