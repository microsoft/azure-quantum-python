##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging

from typing import Optional

from azure.quantum.target.solvers import RangeSchedule, Solver
from azure.quantum.workspace import Workspace

logger = logging.getLogger(__name__)

class SubstochasticMonteCarlo(Solver):
    target_names = (
        "microsoft.substochasticmontecarlo.cpu",
        "microsoft.substochasticmontecarlo-parameterfree.cpu",
    )
    def __init__(
        self,
        workspace: Workspace,
        name: str = "microsoft.substochasticmontecarlo.cpu",
        alpha: Optional[RangeSchedule] = None,
        seed: Optional[int] = None,
        target_population: Optional[int] = None,
        step_limit: Optional[int] = None,
        beta: Optional[RangeSchedule] = None,
        steps_per_walker: Optional[int] = None,
        timeout: Optional[int] = None,
        **kwargs
    ):
        """Constructor of Substochastic Monte Carlo solver.

        Substochastic Monte Carlo solver for binary optimization problems
        with k-local interactions on an all-to-all graph topology with double
        precision support for the coupler weights.

        This solver is CPU only.

        :param alpha:
            Evolution of alpha (chance to step) over time.
            Must be an object of type RangeSchedule describing a
            decreasing probability (1 >= initial > final >= 0).
        :param seed:
            Specifies the random number generator seed value.
        :target_population:
            Target size of the population. Must be positive.
        :param step_limit:
            Number of Monte Carlo steps (not sweeps!). Must be positive.
        :param beta:
            Evolution of beta (resampling factor) over time.
            Must be an object of type RangeSchedule describing
            an increasing evolution (0 < initial < final)
        :param steps_per_walker:
            Number of steps to attempt for each walker. Must be positive.
        :param timeout:
            Specifies maximum number of seconds to run the core solver
            loop. Initialization time does not respect this value, so the
            solver may run longer than the value specified. Setting this value
            will trigger the parameter free substochastic monte carlo solver.
        """

        if timeout is not None:
            name = "microsoft.substochasticmontecarlo-parameterfree.cpu"
        super().__init__(
            workspace=workspace,
            provider_id="Microsoft",
            name=name,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2",
            **kwargs
        )
        self.set_one_param("seed", seed)
        self.check_set_positive_int("steps_per_walker", steps_per_walker)
        self.check_set_positive_int("target_population", target_population)
        self.check_set_positive_int("step_limit", step_limit)
        self.check_set_schedule(
                "alpha", alpha, evolution=self.ScheduleEvolution.DECREASING,
                lower_bound_inclusive=0)
        self.check_set_schedule(
                "beta", beta, evolution=self.ScheduleEvolution.INCREASING,
                lower_bound_exclusive=0)
        self.check_set_positive_int("timeout", timeout)
    
    def supports_grouped_terms(self):
        return True
    
    def supports_protobuf(self):
        return True
