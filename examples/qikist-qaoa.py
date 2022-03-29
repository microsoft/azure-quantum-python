##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor

from azure.quantum.qiskit import AzureQuantumProvider

# from qiskit import IBMQ
# IBMQ.load_account()
# provider = IBMQ.get_provider(hub='ibm-q', group='open', project='main')
# backend = provider.get_backend('ibmq_qasm_simulator')

# Azure Quantum Provider
provider = AzureQuantumProvider(
  resource_id="/subscriptions/916dfd6d-030c-4bd9-b579-7bb6d1926e97/resourceGroups/anpaz-demos/providers/Microsoft.Quantum/Workspaces/demo15",
  location="westus"
)
backend = provider.get_backend('ionq.simulator')

from qiskit.utils import QuantumInstance
from qiskit.algorithms import QAOA
from qiskit.algorithms.optimizers import COBYLA

from qiskit_optimization import QuadraticProgram
from qiskit_optimization.algorithms import MinimumEigenOptimizer

qp = QuadraticProgram()
qp.binary_var("x")
qp.binary_var("y")
qp.binary_var("z")
qp.minimize(linear=[1, -2, 3], quadratic={("x", "y"): 1, ("x", "z"): -1, ("y", "z"): 2})
print(qp.export_as_lp_string())

seed = 42
cobyla = COBYLA()
cobyla.set_options(maxiter=250)
qaoa_mes = QAOA(optimizer=cobyla, reps=3, quantum_instance=backend)
qaoa = MinimumEigenOptimizer(qaoa_mes)
result = qaoa.solve(qp)

