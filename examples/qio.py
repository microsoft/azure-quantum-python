from azure.quantum import __version__
print(__version__)


from azure.quantum import Workspace
from azure.quantum.optimization import Problem, Term
from azure.quantum.optimization.problem import ProblemType
from azure.quantum.optimization.solvers import SimulatedAnnealing, ParallelTempering, QuantumMonteCarlo, Tabu

#from azure.common.credentials import ServicePrincipalCredentials
from azure.identity import ClientSecretCredential, EnvironmentCredential,AzureCliCredential

workspace = Workspace(
    resource_id="/subscriptions/f22ec525-2e94-482f-a69a-d2de1f292c19/resourceGroups/rg-masenol-6d532/providers/Microsoft.Quantum/Workspaces/ws-06872a4b-85d8-498e-9ccc-3076aa2b5a2f",
    location = "westus"
#    credential = AzureCliCredential()
)
print()
print(workspace.name)
print(workspace.get_targets())
exit()

workspace = Workspace(
    resource_id="/subscriptions/916dfd6d-030c-4bd9-b579-7bb6d1926e97/resourceGroups/anpaz-demos/providers/Microsoft.Quantum/Workspaces/demo15",
    location = "westus",
    credential = AzureCliCredential()
)
print()
print(workspace.name)
print(workspace.get_targets())

workspace = Workspace(
    resource_id="/subscriptions/677fc922-91d0-4bf6-9b06-4274d319a0fa/resourceGroups/xiou/providers/Microsoft.Quantum/Workspaces/xiou-notebooks-demo",
    location = "eastus2euap",
    credential = AzureCliCredential()
)
print()
print(workspace.name)
print(workspace.get_targets())

exit()


## Create a problem:
terms = [
    Term(w=-3, indices=[1,0]),
    Term(w=5, indices=[2,0]),
    Term(w=9, indices=[2,1]),
    Term(w=2, indices=[3,0]),
    Term(w=-4, indices=[3,1]),
    Term(w=4, indices=[3,2])
]
initial_config = {
    "1":-1,
    "0":1,
    "2":-1,
    "3":1
}
problem = Problem(name="e2e-basic_microsoft", terms = terms, init_config=initial_config)

solver = SimulatedAnnealing(workspace)

job = solver.submit(problem)
print(job.id)



job.wait_until_completed()
results = job.get_results()