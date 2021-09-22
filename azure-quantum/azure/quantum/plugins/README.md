# Python SDK for Azure Quantum Plugins #

For details on how to get started with Azure Quantum, please visit [azure.com/quantum](https://azure.com/quantum).

You can also try our [Quantum Computing Fundamentals](https://aka.ms/learnqc) learning path to get familiar with the basic concepts of quantum computing, build quantum programs, and identify the kind of problems that can be solved.

This folder contains plug-ins to the Python SDK for Azure Quantum.

### Installing with pip ###

To install all plugins, run:

```bash
pip install azure-quantum[cirq,qiskit]
```

this will install the plugins along with their optional dependencies.

## The `cirq` plugin ##

This plugin lets you use Azure Quantum as a service in  `cirq` to run quantum programs.

### Example usage ###

```python
import cirq
import azure.quantum.cirq as aq

# Create qubits
q0 = cirq.LineQubit(0)
q1 = cirq.LineQubit(1)
q2 = cirq.LineQubit(2)

# Create a circuit
circuit = cirq.Circuit(
    cirq.H(q0),  # H gate
    cirq.CNOT(q0, q1),
    cirq.CNOT(q1, q2),
    cirq.measure(q0, key='q0'),
    cirq.measure(q1, key='q1'),
    cirq.measure(q2, key='q2'),
)

# Enter your Azure Quantum workspace details here
service = aq.AzureQuantumService(resource_id="", location="")
result = service.run(circuit, repetitions=1000, target="ionq.simulator")
```

### Installing with pip ###

```bash
pip install azure-quantum[cirq]
```

## The `qiskit` plugin ##

This package implements an `AzureQuantumProvider` class that supports submitting `qiskit` circuits to Azure Quantum targets.

### Example usage ###

```python
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from azure.quantum.qiskit import AzureQuantumProvider

# Azure Quantum Provider
# Find your resource ID via portal.azure.com
provider = AzureQuantumProvider(
  resource_id="",
  location=""
)

# Show all current supported backends in this workspace:
print([backend.name() for backend in provider.backends()])

# Get IonQ's simulator backend:
simulator_backend = provider.get_backend("ionq.simulator")

# Create a Quantum Circuit acting on the q register
circuit = QuantumCircuit(2, 2)
circuit.name = "Qiskit Sample - Bell circuit"
circuit.h(0)
circuit.cx(0, 1)
circuit.measure([0,1], [0, 1])

# Submit the circuit to run on Azure Quantum
job = simulator_backend.run(circuit, shots=250)
job_id = job.id()
print("Job id", id)

# Get the job results (this method waits for the Job to complete):
counts = result.get_counts(circuit)
print(counts)

# Plot histogram
plot_histogram(counts)
```

### Installing with pip ###

```bash
pip install azure-quantum[qiskit]
```

### Development ###

The best way to install all the Python pre-reqs packages is to create a new Conda environment.
Run at the root of the `azure-quantum` directory:

```bash
conda env create -f environment.yml
```

Then to activate the environment:

```bash
conda activate azurequantum
```

In case you have created the conda environment a while ago, you can make sure you have the latest versions of all dependencies by updating your environment:

```bash
conda env update -f environment.yml --prune
```

#### Install the local development package ####

To install the package in development mode, run the following in the repo's root directory:

```bash
pip install -e azure-quantum[qiskit]
```

## Support and Q&A ##

If you have questions about the Quantum Development Kit and the Q# language, or if you encounter issues while using any of the components of the kit, you can reach out to the quantum team and the community of users in [Stack Overflow](https://stackoverflow.com/questions/tagged/q%23) and in [Quantum Computing Stack Exchange](https://quantumcomputing.stackexchange.com/questions/tagged/q%23) tagging your questions with **q#**.
