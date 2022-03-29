##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from qiskit import QuantumCircuit, transpile
from qiskit.circuit.random import random_circuit
from qiskit.providers.ibmq.managed import IBMQJobManager
from qiskit.tools.monitor import job_monitor

from qiskit import IBMQ
provider = IBMQ.load_account()
backend = provider.get_backend('ibmq_qasm_simulator')

# Azure Quantum Provider: NOT SUPPORTED BY JobManager
# from azure.quantum.qiskit import AzureQuantumProvider
# provider = AzureQuantumProvider(
#   resource_id="/subscriptions/916dfd6d-030c-4bd9-b579-7bb6d1926e97/resourceGroups/anpaz-demos/providers/Microsoft.Quantum/Workspaces/demo15",
#   location="westus"
# )
# backend = provider.get_backend("ionq.simulator")

# Use Job Manager to retrieve existing job set
job_manager = IBMQJobManager()
job_set_foo = job_manager.retrieve_job_set("3f54467186434e44908fa51220ab266c-16485800905683696", provider)
print(job_set_foo)

# Build a couple of circuits.
circs = []
for _ in range(4):
    circs.append(random_circuit(num_qubits=5, depth=4, measure=True))


# Need to transpile the circuits first.
circs = transpile(circs, backend=backend)

# ## No need to use JobManager, you can submit multiple circuits on the same Job:
# job = backend.run(circs)
# print(job)
# job_monitor(job)

# Use Job Manager to break the circuits into multiple jobs.
job_manager = IBMQJobManager()
job_set_foo = job_manager.run(circs, backend=backend, name='foo')


# Get the job results (this method also waits for the Job to complete):
job, idx = job_set_foo.job(0)
job_monitor(job)

result = job.result()
print(result)
counts = result.get_counts(circs[3])
print(counts)

