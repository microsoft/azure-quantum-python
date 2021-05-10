# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

##
# Integration tests for connecting to the
# Azure Quantum service and solving Optimization problems.
##

import os
import configparser
import functools
from integration_test_util import create_workspace

from azure.quantum import Workspace
from azure.quantum.optimization import (
    Problem,
    ProblemType,
    Term,
    ParallelTempering,
    SimulatedAnnealing,
    Tabu,
    QuantumMonteCarlo,
    PopulationAnnealing,
    SubstochasticMonteCarlo
)
from azure.quantum.optimization.oneqbit import (
    TabuSearch,
    PticmSolver,
    PathRelinkingSolver,
)

from azure.quantum.optimization.toshiba import SimulatedBifurcationMachine


def create_problem(init: bool = False) -> Problem:
    """Create optimization problem with some default terms

    :param init: Set initial configuration
    :type init: bool
    :return: Optimization problem
    :rtype: Problem
    """
    terms = [
        Term(w=-3, indices=[1, 0]),
        Term(w=5, indices=[2, 0]),
        Term(w=9, indices=[2, 1]),
        Term(w=2, indices=[3, 0]),
        Term(w=-4, indices=[3, 1]),
        Term(w=4, indices=[3, 2]),
    ]

    if init is True:
        initial_config = {"1": 0, "0": 1, "2": 0, "3": 1}

        return Problem(
            name="initial_condition_demo",
            terms=terms,
            init_config=initial_config,
            problem_type=ProblemType.pubo,
        )

    else:
        return Problem(
            name="first-demo", terms=terms, problem_type=ProblemType.pubo
        )


def solve(
    problem: Problem, solver_name: str, solver_factory: callable
) -> None:
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

    # Call optimize on a solver to find the solution of a problem:
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
        "QuantumMonteCarlo",
        "PopulationAnnealing",
        "SubstochasticMonteCarlo"
    ]

    solvers = [
        functools.partial(SimulatedAnnealing, beta_start=0),
        functools.partial(ParallelTempering, sweeps=100),
        functools.partial(Tabu, sweeps=100),
        functools.partial(QuantumMonteCarlo, trotter_number=1),
        functools.partial(PopulationAnnealing, sweeps=200),
        functools.partial(SubstochasticMonteCarlo, step_limit=280)
    ]

    # Check if 1QBit solvers are enabled
    one_qbit_enabled = os.environ.get("AZURE_QUANTUM_1QBIT", "") == "1"

    if one_qbit_enabled:
        print("1QBit solver is enabled.")
        names += ["TabuSearch", "PticmSolver", "PathRelinkingSolver"]

        solvers += [
            functools.partial(TabuSearch, improvement_cutoff=10),
            functools.partial(PticmSolver, num_sweeps_per_run=99),
            functools.partial(PathRelinkingSolver, distance_scale=0.44),
        ]
    # Check if Toshiba solvers are enabled
    toshiba_enabled = os.environ.get("AZURE_QUANTUM_TOSHIBA", "") == "1"

    if toshiba_enabled:
        print("Toshiba solver is enabled.")
        names += ["SimulatedBifurcationMachine"]

        solvers += [
            functools.partial(SimulatedBifurcationMachine, loops=10),
        ]

    # Create problems
    problems = [create_problem(), create_problem(init=True)]

    for name, get_solver in zip(names, solvers):
        for problem in problems:
            solve(problem=problem, solver_name=name, solver_factory=get_solver)
