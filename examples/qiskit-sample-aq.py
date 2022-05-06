##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor

from azure.quantum.qiskit import AzureQuantumProvider
from azure.quantum.target.rigetti import RigettiTarget

from azure.quantum import Workspace

# Azure Quantum Provider
provider = AzureQuantumProvider(
  resource_id="/subscriptions/916dfd6d-030c-4bd9-b579-7bb6d1926e97/resourceGroups/anpaz-demos/providers/Microsoft.Quantum/Workspaces/demo16",
  location="eastus2euap"
)

# provider = AzureQuantumProvider(
#   resource_id="/subscriptions/677fc922-91d0-4bf6-9b06-4274d319a0fa/resourceGroups/xiou/providers/Microsoft.Quantum/Workspaces/xiou-notebooks-demo",
#   location="eastus2euap"
# )

# job = workspace.get_job('05de4674-c196-11ec-8a2a-d4d25276417e')
# rawOutput = job.download_blob("rawOutputData")
# print("rawOutput: ")
# print(rawOutput)
# exit(0)

# Show all current supported backends in this workspace:
print([backend.name() for backend in provider.backends()])
backend = provider.get_backend("qci.simulator")
#backend = provider.get_backend("rigetti.sim.qvm")
#backend = provider.get_backend("quantinuum.hqs-lt-s1-apival")

# job = backend.retrieve_job('ca3ecb76-cb29-11ec-b2e4-2a16a847b8a3')
# print(job._azure_job.details.error_data)
# print(job._azure_job.download_attachment('rawOutputData').decode('utf-8'))
# exit(0)

# job = backend.retrieve_job('8ba68e8c-c818-11ec-bde0-2a16a847b8a3')
# result = job.result()
# print(job._azure_job.details)
# print('------------------------')
# print(result)
# counts=result.get_counts()
# print('------------------------')
# print(counts)
# plot_histogram(counts)
# exit(0)

# Create a Quantum Circuit acting on the q register
circuit = QuantumCircuit(2, 2)
circuit.name = "Qiskit Sample - Bell circuit"
circuit.h(0)
circuit.cx(0, 1)
circuit.measure([0,1], [0, 1])

from qiskit_qir import to_qir_bitcode, to_qir
print(to_qir(circuit))

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

# # Read results:
# result = job.result()
# print(result)


# Get the job results (this method also waits for the Job to complete):
result = job.result()
print(result)
counts = result.get_counts(circuit)
print(counts)
plot_histogram(counts)

# # fetch an existing job and show the results:
# job = provider.get_job('89ab5eab-9dca-4cc7-9406-196190a55d98') # iq#
# job = provider.get_job('3bfad3a8-f67b-11eb-a6ee-f01dbc9fb65d') # qiskit qpu
# # Optionally, get the job from the backend:
# job = backend.retrieve_job('7dd53994-c0f7-11ec-97b2-d4d25276417e') # qiskit sim
# result = job.result()
# print(job._azure_job.details)
# print('------------------------')
# print(result)
# counts=result.get_counts()
# print('------------------------')
# print(counts)
# plot_histogram(counts)


# # For jobs that return plain text:
# from azure.quantum import Workspace
# workspace =  Workspace(
#   resource_id="/subscriptions/916dfd6d-030c-4bd9-b579-7bb6d1926e97/resourceGroups/anpaz-demos/providers/Microsoft.Quantum/Workspaces/demo16",
#   location="eastus2euap"
# )
# job = provider.get_job('7dd53994-c0f7-11ec-97b2-d4d25276417e')
# result = job._azure_job.get_results()
# print(result)


