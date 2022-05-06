##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from qiskit import QuantumCircuit
from qiskit.tools.monitor import job_monitor
from azure.quantum.qiskit import AzureQuantumProvider
from azure.quantum import Workspace

# Azure Quantum Provider
provider = AzureQuantumProvider(
  resource_id="/subscriptions/916dfd6d-030c-4bd9-b579-7bb6d1926e97/resourceGroups/anpaz-demos/providers/Microsoft.Quantum/Workspaces/demo16",
  location="eastus2euap"
)

# Show all current supported backends in this workspace:
backend = provider.get_backend("qci.simulator")

# Create a Quantum Circuit acting on the q register
circuit = QuantumCircuit(2, 2)
circuit.name = "Qiskit Sample - Bell circuit"
circuit.h(0)
circuit.cx(0, 1)
circuit.measure([0,1], [0, 1])

# Print out the circuit
print("================== Running circuit: ==================")
print(circuit.draw())
print("======================================================")

# Submit the circuit to run on Azure Quantum
job = backend.run(circuit)
id = job.id()
print("Job id", id)

# Monitor job progress and wait until complete:
job_monitor(job)

# Read results:
result = job.result()
print(result)
counts = result.get_counts(circuit)
print(counts)