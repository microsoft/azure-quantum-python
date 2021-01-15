from azure.quantum import Workspace
from azure.quantum.optimization import Problem, ProblemType, Term, ParallelTempering, SimulatedAnnealing

# put in values for a non-AAD account here
wsMSA = Workspace(
    subscription_id="",
    resource_group="",
    name="",
    storage="")

# ashwinm@microsoft.com - AAD
wsAAD = Workspace(
    subscription_id="",
    resource_group="",
    name="",
    storage="")

ws = wsMSA #or wsAAD
print(ws.name)

# try to login - this should trigger the device flow
ws.login (False)

# create a problem to solve
terms = [
    Term(w=-3, indices=[1,0]),
    Term(w=5, indices=[2,0]),
    Term(w=9, indices=[2,1]),
    Term(w=2, indices=[3,0]),
    Term(w=-4, indices=[3,2]),
    Term(w=4, indices=[3,1])
]

problem = Problem(name="My First Problem", problem_type=ProblemType.ising)
problem.add_terms(terms=terms)

solver = ParallelTempering(ws, timeout=100)

# Solve the problem
result = solver.optimize(problem)

# result should be {'energy': -4.0, 'solution': [0, 0, 1, 1]}
print(result)
