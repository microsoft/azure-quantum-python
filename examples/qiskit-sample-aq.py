##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor

from azure.quantum.qiskit import AzureQuantumProvider

from math import pi
from qiskit_experiments.library import StateTomography
from qiskit_experiments.framework import ParallelExperiment

import qiskit

# Azure Quantum Provider
provider = AzureQuantumProvider(
  resource_id="/subscriptions/916dfd6d-030c-4bd9-b579-7bb6d1926e97/resourceGroups/anpaz-demos/providers/Microsoft.Quantum/Workspaces/demo15",
  location="westus"
)

# provider = AzureQuantumProvider(
#   resource_id="/subscriptions/677fc922-91d0-4bf6-9b06-4274d319a0fa/resourceGroups/xiou/providers/Microsoft.Quantum/Workspaces/xiou-notebooks-demo",
#   location="eastus2euap"
# )

# Show all current supported backends in this workspace:
print([backend.name() for backend in provider.backends()])
backend = provider.get_backend("ionq.simulator")


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
job = backend.run(circuit, memory=True)
id = job.id()
print("Job id", id)

# Monitor job progress and wait until complete:
job_monitor(job)

# Get the job results (this method also waits for the Job to complete):
result = job.result()
print(result)
counts = result.get_counts(circuit)
print(counts)
plot_histogram(counts)

# # fetch an existing job and show the results:
# job = provider.get_job('75379b1e-f676-11eb-ac02-f01dbc9fb65d') # qiskit sim
# job = provider.get_job('89ab5eab-9dca-4cc7-9406-196190a55d98') # iq#
# job = provider.get_job('3bfad3a8-f67b-11eb-a6ee-f01dbc9fb65d') # qiskit qpu
# # Optionally, get the job from the backend:
# job =simulator_backend.retrieve_job('75379b1e-f676-11eb-ac02-f01dbc9fb65d') # qiskit sim
# print(job._azure_job.details)
# result = job.result()
# print('------------------------')
# print(result)
# counts=result.get_counts()
# print('------------------------')
# print(counts)
# plot_histogram(counts)

