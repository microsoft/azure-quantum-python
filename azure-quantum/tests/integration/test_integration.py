# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

##
# Integration tests for connecting to the Azure Quantum service and solving Optimization problems.
##

import os
import configparser
import functools
from azure.common.credentials import ServicePrincipalCredentials

from azure.quantum import Workspace
from azure.quantum.optimization import (
    Problem,
    ProblemType,
    Term,
    ParallelTempering,
    SimulatedAnnealing,
    Tabu,
    QuantumMonteCarlo
)
from azure.quantum.optimization.oneqbit import (
    TabuSearch,
    PticmSolver,
    PathRelinkingSolver
)

from azure.quantum.optimization.toshiba import (
    SimulatedBifurcationMachine
)

def create_workspace() -> Workspace:
    """Create workspace using credentials stored in config file

    :return: Workspace
    :rtype: Workspace
    """

    client_id = os.environ.get("AZURE_CLIENT_ID","")
    client_secret = os.environ.get("AZURE_CLIENT_SECRET","")
    tenant_id = os.environ.get("AZURE_TENANT_ID","")
    resource_group = os.environ.get("RESOURCE_GROUP","")
    subscription_id = os.environ.get("SUBSCRIPTION_ID","")
    workspace_name = os.environ.get("WORKSPACE_NAME","")

    assert len(client_id)>0, "AZURE_CLIENT_ID not found in environment variables."
    assert len(client_id)>0, "AZURE_CLIENT_SECRET not found in environment variables."
    assert len(client_id)>0, "AZURE_TENANT_ID not found in environment variables."
    assert len(client_id)>0, "RESOURCE_GROUP not found in environment variables."
    assert len(client_id)>0, "SUBSCRIPTION_ID not found in environment variables."
    assert len(client_id)>0, "WORKSPACE_NAME not found in environment variables."

    if len(client_secret) > 0:
        workspace = Workspace(
            
            subscription_id=subscription_id,
            resource_group=resource_group,
            name=workspace_name,
        )
        workspace.credentials = ServicePrincipalCredentials(
            tenant=tenant_id,
            client_id=client_id,
            secret=client_secret,
            resource  = "https://quantum.microsoft.com"
        )

    workspace.login()
    return workspace


def create_problem(init: bool = False) -> Problem:
    """Create optimization problem with some default terms

    :param init: Set initial configuration
    :type init: bool
    :return: Optimization problem
    :rtype: Problem
    """
    terms = [
        Term(w=-3, indices=[1,0]),
        Term(w=5, indices=[2,0]),
        Term(w=9, indices=[2,1]),
        Term(w=2, indices=[3,0]),
        Term(w=-4, indices=[3,1]),
        Term(w=4, indices=[3,2])
    ]

    if init is True:
        initial_config = {
            "1": -1,
            "0": 1,
            "2": -1,
            "3": 1
        }

        return Problem(name="initial_condition_demo", terms = terms, init_config=initial_config, problem_type = ProblemType.pubo) 

    else:
        return Problem(name = "first-demo", terms=terms, problem_type = ProblemType.pubo)


def solve(problem: Problem, solver_name: str, solver_factory: callable) -> None:
    """Solve the problem with the given solver

    :param problem Problem to solve
    :type problem: Problem
    :param solver_name: Solver name
    :type solver_name: str
    :param solver_factory: Lambda function that generates a solver 
    from a workspace object
    :type solver_factory: callable
    """
    ws = create_workspace()
    
    ## Call optimize on a solver to find the solution of a problem:
    print("Finding solution...")
    solver = solver_factory(ws)
    print(solver)
    job = solver.submit(problem)
    solution = job.get_results()
    print(f"Solution found ({solver_name}):")
    print(f" -> solution: {solution}")

    print("Download old results:")
    job = ws.get_job(job.id)
    results = job.get_results()
    print("Job results:")
    print(f" -> solution: {results}")


if __name__ == "__main__":
    names = [
        "SimulatedAnnealing",
        "ParallelTempering",
        "Tabu",
        "QuantumMonteCarlo"
    ]

    solvers = [
        functools.partial(SimulatedAnnealing, beta_start=0),
        functools.partial(ParallelTempering, sweeps=100),
        functools.partial(Tabu, sweeps=100),
        functools.partial(QuantumMonteCarlo, trotter_number=1)
    ]

    # Check if 1QBit solvers are enabled
    one_qbit_enabled = os.environ.get("AZURE_QUANTUM_1QBIT", "") == "1"

    if one_qbit_enabled:
        print("1QBit solver is enabled.")
        names += [
            "TabuSearch",
            "PticmSolver",
            "PathRelinkingSolver"
        ]

        solvers += [
            functools.partial(TabuSearch, improvement_cutoff=10),
            functools.partial(PticmSolver, num_sweeps_per_run=99),
            functools.partial(PathRelinkingSolver, distance_scale=0.44),
        ]
    # Check if Toshiba solvers are enabled
    toshiba_enabled = os.environ.get("AZURE_QUANTUM_TOSHIBA", "") == "1"

    if toshiba_enabled:
        print("Toshiba solver is enabled.")
        names += [
            "SimulatedBifurcationMachine"
        ]

        solvers += [
            functools.partial(SimulatedBifurcationMachine, loops=10),
        ]

    # Create problems
    problems = [
        create_problem(),
        create_problem(init=True)
    ]

    for name, get_solver in zip(names, solvers):
        for problem in problems:
            solve(problem=problem, solver_name=name, solver_factory=get_solver)
