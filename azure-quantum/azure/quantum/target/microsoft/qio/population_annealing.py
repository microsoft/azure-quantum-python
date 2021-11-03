##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging

from typing import Optional

from azure.quantum import Workspace
from azure.quantum.target.solvers import RangeSchedule, Solver

logger = logging.getLogger(__name__)

class PopulationAnnealing(Solver):
    target_names = (
        "microsoft.populationannealing.cpu",
        "microsoft.populationannealing-parameterfree.cpu",
    )
    def __init__(
        self,
        workspace: Workspace,
        name: str = "microsoft.populationannealing.cpu",
        alpha: Optional[float] = None,
        seed: Optional[int] = None,
        population: Optional[int] = None,
        sweeps: Optional[int] = None,
        beta: Optional[RangeSchedule] = None,
        timeout: Optional[int] = None,
        **kwargs
    ):
        """Constructor of the Population Annealing solver.

        Population Annealing Search solver for binary optimization problems
        with k-local interactions on an all-to-all graph topology with double
        precision support for the coupler weights.

        This solver is CPU only.

        :param alpha:
            Ratio to trigger a restart. Must be larger than 1.
        :param seed:
            Specifies the random number generator seed value.
        :population:
            Size of the population. Must be positive.
        :param sweeps:
            Number of Monte Carlo sweeps. Must be positive.
        :param beta:
            Evolution of the inverse annealing temperature.
            Must be an object of type RangeSchedule describing
            an increasing evolution (0 < initial < final).
        :param timeout:
            specifies maximum number of seconds to run the core solver
            loop. initialization time does not respect this value, so the
            solver may run longer than the value specified. Setting this value
            will trigger the parameter free population annealing solver.
        """

        if timeout is not None:
            name = "microsoft.populationannealing-parameterfree.cpu"

        super().__init__(
            workspace=workspace,
            provider_id="Microsoft",
            name=name,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2",
            **kwargs
        )

        self.check_set_float("alpha", alpha, lower_bound_exclusive=1.0)
        self.set_one_param("seed", seed)
        self.check_set_positive_int("population", population)
        self.check_set_positive_int("sweeps", sweeps)
        self.check_set_schedule(
                "beta", beta, evolution=self.ScheduleEvolution.INCREASING,
                lower_bound_exclusive=0)
        self.check_set_positive_int("timeout", timeout)

    def supports_grouped_terms(self):
        return True
    
    def supports_protobuf(self):
        return True