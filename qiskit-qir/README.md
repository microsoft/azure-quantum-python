# qiskit-qir

Qiskit to QIR translator.

## Example

```python
from qiskit import QuantumCircuit
from qiskit_qir import to_qir

circuit = QuantumCircuit(name="my-circuit")
circuit.h(0)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.measure([0,1,2], [0, 1, 2])

qir = to_qir(circuit)
```

## Install from source

To install the package from source, clone the repo onto your machine, browse to `qdk-python/qiskit-qir` and run

```bash
pip install -e .
```
