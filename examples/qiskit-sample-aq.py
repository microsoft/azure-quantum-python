from qiskit import QuantumCircuit
from qiskit.providers import JobStatus

from azure.quantum import Workspace
from azure.quantum_qiskit import AzureQuantumProvider

from azure.identity import AzureCliCredential
import time

from qiskit.providers import backend

# Azure Quantum Target
workspace = Workspace(
  resource_id="/subscriptions/916dfd6d-030c-4bd9-b579-7bb6d1926e97/resourceGroups/anpaz-demos/providers/Microsoft.Quantum/Workspaces/demo15",
  location="westus",
  credential=AzureCliCredential()
)
provider = AzureQuantumProvider(workspace)

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
print(id)
#exit()

# Get the job results (this method waits for the Job to complete):
result = job.result()

# Print the results.
print(result)

# fetch an existing job:
job = provider.get_job(id)
result = job.result()
print(result)
exit()