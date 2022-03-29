##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import qiskit
from math import pi
from qiskit import QuantumCircuit
from azure.quantum.qiskit import AzureQuantumProvider
from qiskit_experiments.library import StateTomography
from qiskit_experiments.framework import ParallelExperiment
from qiskit_experiments.framework.experiment_data import ExperimentData


from qiskit import IBMQ
IBMQ.load_account()
provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
backend = provider.get_backend('ibmq_qasm_simulator')

# # Azure Quantum Provider
# provider = AzureQuantumProvider(
#   resource_id="/subscriptions/916dfd6d-030c-4bd9-b579-7bb6d1926e97/resourceGroups/anpaz-demos/providers/Microsoft.Quantum/Workspaces/demo15",
#   location="westus"
# )
# backend = provider.get_backend("ionq.simulator")

# ###########################
# # One Tomograph Experiment
# ###########################
circuit = QuantumCircuit(1)
circuit.h(0)
experiment = StateTomography(circuit)

# Azurequantum cost:
# circuits = qiskit.transpile(experiment.circuits(), backend)
# for c in circuits:
#     cost = backend.estimate_cost(c, shots=1000)
#     print(cost)

qstdata1 = experiment.run(backend, shots=100).block_for_results()
print(qstdata1)
state_result = qstdata1.analysis_results("state")
print(state_result.value)
exit(0)

###########################
# Multiple parallel experiments
###########################
num_qubits = 5
gates = [qiskit.circuit.library.RXGate(i * pi / (num_qubits - 1))
         for i in range(num_qubits)]

subexps = [
    StateTomography(gate, qubits=[i])
    for i, gate in enumerate(gates)
]
experiment = ParallelExperiment(subexps)

pardata = experiment.run(backend, seed_simulation=100).block_for_results()
for result in pardata.analysis_results():
    print(result)
exit(0)

########
# Async running
#######


# Create a Quantum Circuit acting on the q register
circuit = QuantumCircuit(1)
circuit.x(0)
experiment = StateTomography(circuit)


# To load from existing job ids:
job_ids = [
    "6b419068-aeb9-11ec-8151-2a16a847b8a3",
    "6ad75f86-aeb9-11ec-b30c-2a16a847b8a3",
    "5e837c2e-aeb9-11ec-8018-2a16a847b8a3"
]
jobs = [backend.retrieve_job(id) for id in job_ids]

data = ExperimentData(experiment=experiment)
data.add_data(jobs)
data = experiment.analysis.run(data)

state_result = data.analysis_results("state")
print(state_result.value)
exit(0)
