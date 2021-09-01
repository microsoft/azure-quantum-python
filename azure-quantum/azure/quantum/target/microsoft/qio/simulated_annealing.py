##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging

from typing import Optional

from azure.quantum.target.solvers import Solver
from azure.quantum.target.solvers import HardwarePlatform
from azure.quantum.workspace import Workspace

logger = logging.getLogger(__name__)


class SimulatedAnnealing(Solver):
    target_names = [
        "microsoft.simulatedannealing-parameterfree.fpga",
        "microsoft.simulatedannealing.fpga",
        "microsoft.simulatedannealing.cpu",
        "microsoft.simulatedannealing-parameterfree.cpu",
    ]
    def __init__(
        self,
        workspace: Workspace,
        name: str = "microsoft.simulatedannealing.cpu",
        beta_start: Optional[float] = None,
        beta_stop: Optional[float] = None,
        sweeps: Optional[int] = None,
        restarts: Optional[int] = None,
        timeout: Optional[int] = None,
        seed: Optional[int] = None,
        platform: Optional[HardwarePlatform] = HardwarePlatform.CPU,
        **kwargs
    ):
        """The constructor of an Simulated Annealing solver.

        Multi-core Simulated Annealing solver for binary optimization problems
        with k-local interactions on an all-to-all graph topology with double
        precision support for the coupler weights.

        :param beta_start:
            specifies the starting inverse temperature.
        :param beta_stop:
            specifies the stopping inverse temperature.
        :param sweeps:
            specifies the number of sweeps.
        :param restarts:
            specifies the number of restarts.
        :param timeout:
            specifies maximum number of seconds to run the core solver
            loop. initialization time does not respect this value, so the
            solver may run longer than the value specified.
        :param seed:
            specifies a random seed value.
        :platform:
            specifies hardware platform
            HardwarePlatform.CPU or HardwarePlatform.FPGA.
        """
        param_free = (
            beta_start is None
            and beta_stop is None
            and sweeps is None
            and restarts is None
        )

        if platform == HardwarePlatform.FPGA:
            name = (
                "microsoft.simulatedannealing-parameterfree.fpga"
                if param_free
                else "microsoft.simulatedannealing.fpga"
            )
        elif param_free:
            name = "microsoft.simulatedannealing-parameterfree.cpu"

        super().__init__(
            workspace=workspace,
            provider_id="Microsoft",
            name=name,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2",
            **kwargs
        )

        self.set_one_param("beta_start", beta_start)
        self.set_one_param("beta_stop", beta_stop)
        self.set_one_param("sweeps", sweeps)
        self.set_one_param("restarts", restarts)
        self.set_one_param("timeout", timeout)
        self.set_one_param("seed", seed)