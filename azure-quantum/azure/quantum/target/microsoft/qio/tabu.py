##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging

from typing import Optional

from azure.quantum.target.solvers import Solver
from azure.quantum.workspace import Workspace

logger = logging.getLogger(__name__)

class Tabu(Solver):
    target_names = (
        "microsoft.tabu.cpu",
        "microsoft.tabu-parameterfree.cpu",
    )
    def __init__(
        self,
        workspace: Workspace,
        name: str = "microsoft.tabu.cpu",
        sweeps: Optional[int] = None,
        tabu_tenure: Optional[int] = None,
        timeout: Optional[int] = None,
        seed: Optional[int] = None,
        restarts: Optional[int] = None,
        **kwargs
    ):
        """The constructor of an Tabu Search solver.

        Multi-core Tabu Search solver for binary optimization problems
        with k-local interactions on an all-to-all graph topology with double
        precision support for the coupler weights.

        This solver is CPU only.

        :param sweeps:
            specifies the number of sweeps.
        :param tabu_tenure:
            specifies the tabu tenure.
        :param restarts:
            specifies how many runs the solver will execute.
        :param timeout:
            specifies maximum number of seconds to run the core solver
            loop. initialization time does not respect this value, so the
            solver may run longer than the value specified.
        :param seed:
            specifies a random seed value.
        """
        if sweeps is None and tabu_tenure is None and restarts is None:
            name = "microsoft.tabu-parameterfree.cpu"

        super().__init__(
            workspace=workspace,
            provider_id="Microsoft",
            name=name,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2",
            **kwargs
        )

        self.set_one_param("sweeps", sweeps)
        self.set_one_param("tabu_tenure", tabu_tenure)
        self.set_one_param("timeout", timeout)
        self.set_one_param("seed", seed)
        self.set_one_param("restarts", restarts)