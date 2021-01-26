##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging
import uuid
import azure.quantum

from typing import List, Union, Any, Optional
from enum import Enum
from azure.quantum import Workspace
from azure.quantum.optimization import Problem, Solver

logger = logging.getLogger(__name__)

__all__ = [
    'TabuSearch',
    'PticmSolver',
    'PathRelinkingSolver'
]

class TabuSearch(Solver):
    def __init__(
        self,
        workspace: Workspace,
        improvement_cutoff: Optional[int]=None,
        improvement_tolerance: Optional[float]=None,
        tabu_tenure: Optional[int]=None,
        tabu_tenure_rand_max: Optional[int]=None,
        timeout: Optional[int]=None
        ):
        """The constructor of a Tabu Search solver.
        
        An iterative heuristic algorithm that uses local search techniques
        to solve a QUBO problem. It starts from a random solution and looks
        for an improved solution in the solution's neighborhood which includes
        all possible single flips. The algorithm stops when it reaches a stopping
        criterion, such as a specified number of consecutive iterations without
        improvement.
        
        For more information please visit:
        https://portal.1qbit.com/docs/model/tabusolver

        :param improvement_cutoff: 
            The number of iterations that the solver attempts with no improvement
            before stopping. Default: 0
        :param improvement_tolerance: 
            The tolerance value that determines if a solution is an improvement
            over the previous iteration. Default: 1e-9
        :param tabu_tenure: 
            The tenure prevents a flipped variable from being flipped again during
            the iterations. Default: 0
        :param tabu_tenure_rand_max: 
            The upper limit of the exclusive range of random integers.
            Valid value range: 1 to 200,000. Default: 0
        :param timeout: 
            The duration in ms the solver runs before exiting. If the value is set
            to 0, it does not time out. Default: 0
        """
        super().__init__(
            workspace=workspace,
            provider="1qbit",
            target="1qbit.tabu",
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v1",
            nested_params=False,
            force_str_params=True)

        self.set_one_param("improvement_cutoff", improvement_cutoff)
        self.set_one_param("improvement_tolerance", improvement_tolerance)
        self.set_one_param("tabu_tenure", tabu_tenure)
        self.set_one_param("tabu_tenure_rand_max", tabu_tenure_rand_max)
        self.set_one_param("timeout", timeout)


class PticmSolver(Solver):
    def __init__(
        self,
        workspace: Workspace,
        auto_set_temperatures: Optional[bool]=None,
        elite_threshold: Optional[float]=None,
        frac_icm_thermal_layers: Optional[float]=None,
        frac_sweeps_fixing: Optional[float]=None,
        frac_sweeps_idle: Optional[float]=None,
        frac_sweeps_stagnation: Optional[float]=None,
        goal: Optional[str]=None,
        high_temp: Optional[float]=None,
        low_temp: Optional[float]=None,
        max_samples_per_layer: Optional[int]=None,
        max_total_sweeps: Optional[int]=None,
        manual_temperatures: Optional[List[float]]=None,
        num_elite_temps: Optional[int]=None,
        num_replicas: Optional[int]=None,
        num_sweeps_per_run: Optional[int]=None,
        num_temps: Optional[int]=None,
        perform_icm: Optional[bool]=None,
        scaling_type: Optional[str]=None,
        var_fixing_type: Optional[str]=None
        ):
        """The constructor of a PTICM solver.
        
        The parallel tempering with isoenergetic cluster moves (PTICM) solver is
        a Monte Carlo approach to solving QUBO problems. In this algorithm, multiple
        replicas of the original system, each with a different initial state, are
        simulated at different temperatures simultaneously. The replicas at
        neighboring temperatures are periodically swapped based on a Metropolis
        criterion. These swaps allow different replicas to do a random walk in the
        temperature space, thereby, efficiently overcoming energy barriers.

        For more information please visit:
        https://portal.1qbit.com/docs/model/pticmsolver

        :param auto_set_temperatures:
            This defines whether the temperature parameters are auto-calculated
            or not. Set it to True for auto-calculating and False for customizing
            the temperature parameters. Default: True
        :param elite_threshold:
            The fraction of the best solutions used for the var_fixing_type
            parameter with value SPVAR. Default: 0.3
        :param frac_icm_thermal_layers:
            The fraction of temperatures for the iso-energetic cluster moves.
            To change this value, set the perform_icm parameter to True.
            Default: 0.5
        :param frac_sweeps_fixing:
            The fraction of sweeps used for fixing the QUBO variables.
            Default: 0.15
        :param frac_sweeps_idle:
            The fraction of sweeps to wait before fixing the QUBO variables.
            Default: 1.0
        :param frac_sweeps_stagnation:
            The fraction of sweeps without improvement that triggers a restart.
            Default: 1.0
        :param goal:
            This defines whether the solver is used for optimizing or sampling.
            Valid values: "OPTIMIZE" or "SAMPLE". Default: "OPTIMIZE"
        :param high_temp:
            The highest temperature of a replica. Set the auto_set_temperatures
            parameter to False to use this feature. Default: 2
        :param low_temp:
            The lowest temperature of a replica. Set the auto_set_temperatures
            parameter to False to use this feature. Default: 0.2
        :param max_samples_per_layer:
            The maximum number of samples collected per replica. Default: 10
        :param max_total_sweeps:
            The total number of sweeps before termination.
            Default: num_sweeps_per_run * 10
        :param manual_temperatures:
            An array of a custom temperature schedule which includes the high,
            intermediate, and low temperature values for the replicas. Set the
            auto_set_temperatures parameter to False to use this feature.
        :param num_elite_temps:
            The number of elite temperatures used for fixing the variables with
            persistency. Default = 4
        :param num_replicas:
            The number of replicas at each temperature. Default: 2
        :param num_sweeps_per_run:
            The number of Monte Carlo sweeps. Default: 100
        :param num_temps:
            The number of temperatures including the highest and the lowest
            temperatures. Set the auto_set_temperatures parameter to False to
            use this feature. Default: 30
        :param perform_icm:
            This defines whether or not to perform the isoenergetic cluster
            moves. Default: True
        :param scaling_type:
            This defines whether the QUBO problem is automatically scaled or not.
            "MEDIAN" means it's automatically scaled, and "NO_SCALING" means it's
            not. Valid values: "MEDIAN" or "NO_SCALING"
        :param var_fixing_type:
            This decides whether the values of QUBO variables are fixed or not.
            You can fix them with "PERSISTENCY" or "SPVAR" types. "NO_FIXING" means the
            variables are not fixed. If you choose "PERSISTENCY" or "SPVAR", also
            set the frac_sweeps_fixing and frac_sweeps_idle parameters to a number
            less than one. Valid values: "PERSISTENCY", "SPVAR" or "NO_FIXING".
            Default: "NO_FIXING"
        """
        super().__init__(
            workspace=workspace,
            provider="1qbit",
            target="1qbit.pticm",
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v1",
            nested_params=False,
            force_str_params=True)

        self.set_one_param("auto_set_temperatures", auto_set_temperatures)
        self.set_one_param("elite_threshold", elite_threshold)
        self.set_one_param("frac_icm_thermal_layers", frac_icm_thermal_layers)
        self.set_one_param("frac_sweeps_fixing", frac_sweeps_fixing)
        self.set_one_param("frac_sweeps_idle", frac_sweeps_idle)
        self.set_one_param("frac_sweeps_stagnation", frac_sweeps_stagnation)
        self.set_one_param("goal", goal)
        self.set_one_param("high_temp", high_temp)
        self.set_one_param("low_temp", low_temp)
        self.set_one_param("max_samples_per_layer", max_samples_per_layer)
        self.set_one_param("max_total_sweeps", max_total_sweeps)
        self.set_one_param("manual_temperatures", manual_temperatures)
        self.set_one_param("num_elite_temps", num_elite_temps)
        self.set_one_param("num_replicas", num_replicas)
        self.set_one_param("num_sweeps_per_run", num_sweeps_per_run)
        self.set_one_param("num_temps", num_temps)
        self.set_one_param("perform_icm", perform_icm)
        self.set_one_param("scaling_type", scaling_type)
        self.set_one_param("var_fixing_type", var_fixing_type)


class PathRelinkingSolver(Solver):
    def __init__(
        self,
        workspace: Workspace,
        distance_scale: Optional[float]=None,
        greedy_path_relinking: Optional[bool]=None,
        ref_set_count: Optional[int]=None,
        timeout: Optional[int]=None
        ):
        """The constructor of a Tabu Search solver.
        
        The path-relinking algorithm is a heuristic algorithm that uses the
        tabu search as a subroutine to solve a QUBO problem. The algorithm
        starts from a set of elite solutions found by the tabu search. It
        then constructs a path between each pair of elite solutions, selects
        one of the solutions along the path, and repeats the tabu search. If
        the tabu search finds a distinct solution that is better than the
        current worst elite solution, the elite solutions set is updated with
        the new improved solution. This whole procedure is repeated until the
        algorithm meets a stopping condition.

        For more information please visit:
        https://portal.1qbit.com/docs/model/pathrelinkingsolver

        :param distance_scale: 
            The minimum distance from the initiating and guiding solutions for
            constructing the candidate solution list. The highest quality
            solution in the candidate solution list is then selected for
            improvement. Valid values: 0.0 to 0.5. Default: 0.33
        :param greedy_path_relinking: 
            When you use the path-relinking solver there are two ways you can
            generate a path that leads to the solution: one is the greedy function
            and the other operates in a random matter. If you set the this
            parameter to true, the solver will use the greedy function. If you
            set it to false, it will use the random method. Default: False
        :param ref_set_count: 
            The number of initial elite solutions to be generated by the tabu
            search algorithm. Valid values: Greater than 1. Default: 10
        :param timeout: 
            The duration in ms the solver runs before exiting. If the value is set
            to 0, it does not time out. Default: 0
        """
        super().__init__(
            workspace=workspace,
            provider="1qbit",
            target="1qbit.pathrelinking",
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v1",
            nested_params=False,
            force_str_params=True)

        self.set_one_param("distance_scale", distance_scale)
        self.set_one_param("greedy_path_relinking", greedy_path_relinking)
        self.set_one_param("ref_set_count", ref_set_count)
        self.set_one_param("timeout", timeout)
