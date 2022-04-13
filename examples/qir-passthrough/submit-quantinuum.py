import os

# Turn on debug logs:
import logging
logging.basicConfig(level=logging.DEBUG)

from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor

from azure.quantum.qiskit import AzureQuantumProvider


# Create a Qiskit's Provider and Backend:
provider = AzureQuantumProvider(
    subscription_id=os.environ["AZURE_QUANTUM_SUBSCRIPTION_ID"],
    resource_group=os.environ["AZURE_QUANTUM_WORKSPACE_RG"],
    name=os.environ["AZURE_QUANTUM_WORKSPACE_NAME"],
    location=os.environ["AZURE_QUANTUM_WORKSPACE_LOCATION"]
)
backend = provider.get_backend("honeywell.hqs-lt-s2-apival")

circuit = QuantumCircuit(3, 3, name="my-circuit")
circuit.h(0)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.measure([0,1,2], [0, 1, 2])

job = backend.run(circuit, input_data_format="qir.v1")

# Print job, wait for results:
print(job.id())

# Monitor job progress and wait until complete:
job_monitor(job)

# Get the job results (this method also waits for the Job to complete):
result = job.result()
print(result)
counts = result.get_counts(circuit)
print(counts)
plot_histogram(counts)


