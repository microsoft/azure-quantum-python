# Submitting IonQ programs to Azure Quantum

This example shows how to create and submit a quantum program to the IonQ Provider via Azure Quantum.

## Generate IonQ format from Qiskit

To generate IonQ JSON from Qiskit, first make sure to install the following dependencies:

```bash
pip install -U "qiskit-terra>=0.17.4"
pip install qiskit-ionq
```

Then, in a Python file, IPython prompt or Jupyter notebook, create a basic circuit using Qiskit, for example:

```python
from qiskit import QuantumCircuit

# Create a basic Bell State circuit:
circuit = QuantumCircuit(2, 2)
circuit.h(0)
circuit.cx(0, 1)
circuit.measure([0, 1], [0, 1])
```

Then, you can translate this circuit directly to IonQ format in Python:

```python
ionq_circ, _, _ = qiskit_circ_to_ionq_circ(circuit)
input_data = json.dumps({
    "qubits": circuit.num_qubits,
    "circuit": ionq_circ,
})
```

## Generate IonQ format from Cirq

To generate IonQ JSON from Cirq, first make sure to install the following dependency:

```bash
pip install cirq-ionq
```

Then, in Python, create a basic circuit using Cirq, for example:

```python
import cirq

# Create qubits
q0 = cirq.LineQubit(0)
q1 = cirq.LineQubit(1)
q2 = cirq.LineQubit(2)

# Create a circuit
circuit = cirq.Circuit(
    cirq.H(qubit),  # H gate
    cirq.CNOT(q0, q1),
    cirq.CNOT(q1, q2),
    cirq.measure(q0, key='q0'),
    cirq.measure(q1, key='q1'),
    cirq.measure(q2, key='q2'),
)
```

Then, translate this circuit to IonQ JSON as follows:

```python
from cirq_ionq.serializer import Serializer

input_data = Serializer().serialize(circuit)
```
