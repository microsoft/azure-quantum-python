##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from qiskit import QuantumCircuit
from azure.quantum_qiskit import AzureQuantumProvider

from utils import plot_results

# Azure Quantum Provider
provider = AzureQuantumProvider(
  resource_id="/subscriptions/916dfd6d-030c-4bd9-b579-7bb6d1926e97/resourceGroups/anpaz-demos/providers/Microsoft.Quantum/Workspaces/demo15",
  location="westus"
)

# Show all current supported backends in this workspace:
print([backend.name() for backend in provider.backends()])

# Get IonQ's simulator backend:
simulator_backend = provider.get_backend("ionq.simulator")

# Create a Quantum Circuit acting on the q register
circuit = QuantumCircuit(2, 2)
circuit.name = "Qiskit Sample - C1"
circuit.h(0)
circuit.cx(0, 1)
circuit.measure([0,1], [0, 1])

# Print out the circuit
print("================== Running circuit: ==================")
print(circuit.draw())
print("======================================================")


# Submit the circuit to run on Azure Quantum
job = simulator_backend.run(circuit, shots=250)
id = job.id()
print("Job id", id)
#exit()

# Get the job results (this method waits for the Job to complete):
result = job.result()
histogram = result.results['histogram']
print()
print("Results histogram", histogram)

# Show the histogram as a plot:
plot_results(job)


# fetch an existing job and show the results:
job = provider.get_job('256f02ca-e934-11eb-87f9-2816a847b9a3')
plot_results(job)
