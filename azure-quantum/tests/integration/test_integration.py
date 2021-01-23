# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

##
# Integration tests for connecting to the Azure Quantum service and solving Optimization problems.
##

import os
import configparser

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


def get_config() -> configparser.ConfigParser:
    """Read config file and return config parser

    :return: Config parser for reading config file
    :rtype: configparser.ConfigParser
    """
    config = configparser.ConfigParser()
    path = os.path.abspath(os.path.join(os.path.split(__file__)[0], "..", ".."))
    config_path = os.path.join(path, "config.ini")
    assert os.path.exists(config_path), "Cannot run integration tests: no config file found in azure-quantum folder."
    config.read(config_path)

    return config


def create_workspace() -> Workspace:
    """Create workspace using credentials stored in config file

    :return: Workspace
    :rtype: Workspace
    """
    config = get_config()
    workspace = Workspace(
        subscription_id=config["azure.quantum"]["subscription_id"],
        resource_group=config["azure.quantum"]["resource_group"],
        name=config["azure.quantum"]["workspace_name"],
        storage="")

    # try to login - this should trigger the device flow
    workspace.login(False)
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

        return Problem(name="initial_condition_demo", terms = terms, init_config=initial_config)

    else:
        return Problem(name = "first-demo", terms=terms)


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
    job = solver.submit(problem)
    solution = job.get_results()
    print(f"Solution found ({solver_name}):")
    print(f" -> cost: {solution['cost']}")
    print(f" -> configuration: {solution['configuration']}")

    print("Download old results:")
    job = ws.get_job(job.id)
    results = job.get_results()
    print("Job results:")
    print(f" -> cost: {results['cost']}")
    print(f" -> configuration: {results['configuration']}")


if __name__ == "__main__":
    names = [
        "SimulatedAnnealing",
        "ParallelTempering",
        "Tabu",
        "QuantumMonteCarlo"
    ]

    solvers = [
        lambda ws: SimulatedAnnealing(ws, beta_start=0),
        lambda ws: ParallelTempering(ws, sweeps=100),
        lambda ws: Tabu(ws, sweeps=100),
        lambda ws: QuantumMonteCarlo(ws, trotter_number=1)
    ]

    # Check if IonQ solvers are enabled
    config = get_config()
    ionq_enabled = config["azure.quantum"].get("ionq_enabled", False)

    if ionq_enabled is True:
        names += [
            "TabuSearch",
            "PticmSolver",
            "PathRelinkingSolver"
        ]

        solvers += [
            lambda ws: TabuSearch(ws, improvement_cutoff=10),
            lambda ws: PticmSolver(ws, num_sweeps_per_run=99),
            lambda ws: PathRelinkingSolver(ws, distance_scale=0.44)
        ]

    # Create problems
    problems = [
        create_problem(),
        create_problem(init=True)
    ]

    for name, get_solver in zip(names, solvers):
        for problem in problems:
            solve(problem=problem, solver_name=name, solver_factory=get_solver)
