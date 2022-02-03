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

qir = to_qir(circuit, filename="output.ll")
```

## Dependencies

This package depends on `pyqir_generator` pre-release v0.1.1a1. Because it's not yet available on PyPI, please install it directly from the GitHub release based on your operating system: https://github.com/qir-alliance/pyqir/releases/tag/v0.1.1a1.

For Windows:

```bash
pip install https://github.com/qir-alliance/pyqir/releases/download/v0.1.1a1/pyqir_generator-0.1.1a1-cp36-abi3-linux_x86_64.whl
```

For MacOS:

```bash
pip install https://github.com/qir-alliance/pyqir/releases/download/v0.1.1a1/pyqir_generator-0.1.1a1-cp36-abi3-macosx_10_7_x86_64.whl
```

For Linux:

```bash
https://github.com/qir-alliance/pyqir/releases/download/v0.1.1a1/pyqir_generator-0.1.1a1-cp36-abi3-linux_x86_64.whl
```

or

```bash
https://github.com/qir-alliance/pyqir/releases/download/v0.1.1a1/pyqir_generator-0.1.1a1-cp36-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```
