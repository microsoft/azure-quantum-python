from qiskit import QuantumCircuit
from azure.quantum import Workspace
from azure.quantum.target import Target
from qiskit_qir import to_qir_bitcode, to_qir

workspace = Workspace(
  resource_id="/subscriptions/677fc922-91d0-4bf6-9b06-4274d319a0fa/resourceGroups/masenol-qir-test/providers/Microsoft.Quantum/Workspaces/masenol-contoso-001",
  location="eastus2euap"
)

# Generate QIR from a Qiskit circuit:
circuit = QuantumCircuit(3, 3)
circuit.name = "Qiskit Sample - Bell circuit"
circuit.h(0)
circuit.cx(0, 1)
circuit.cx(0, 2)
circuit.measure([0,1,2], [0,1,2])
qir = to_qir(circuit, "BaseProfileExecution")
print(qir)


echo_target = Target(
    workspace= workspace,
    name= "echo-rigetti",
    input_data_format ="rigetti.qir.v1",
    output_data_format = "rigetti.qir.v1",
    provider_id = "Contoso-QC",
    content_type = "rigetti.qir.v1",
)

job = echo_target.submit(qir, "echo test")
print(job.id)
job.wait_until_completed()
print()
print(job.details.status)

if job.details.status == "Succeeded":
    print()
    print("RESPONSE:")
    print("-------------------------------------------------------------------------")
    results = job.get_results()
    print(results)