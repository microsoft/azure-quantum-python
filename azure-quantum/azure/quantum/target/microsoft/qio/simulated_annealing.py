##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging
from multiprocessing.sharedctypes import Value

from typing import Optional

from azure.quantum.target.solvers import Solver
from azure.quantum.target.solvers import HardwarePlatform
from azure.quantum.workspace import Workspace
from azure.quantum._client.models import TargetStatus

logger = logging.getLogger(__name__)


class SimulatedAnnealing(Solver):
    target_names = [
        "microsoft.simulatedannealing-parameterfree.fpga",
        "microsoft.simulatedannealing.fpga",
        "microsoft.simulatedannealing.cpu",
        "microsoft.simulatedannealing-parameterfree.cpu",
        "microsoft.simulatedannealing.cpu.legacy",
        "microsoft.simulatedannealing-parameterfree.cpu.legacy"
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
            name = name.replace(".simulatedannealing.", ".simulatedannealing-parameterfree.")

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

    @classmethod
    def from_target_status(
        cls, workspace: "Workspace", status: TargetStatus, **kwargs
    ):
        """Create a SimulatedAnnealing instance from a given workspace and target status.

        :param workspace: Associated workspace
        :type workspace: Workspace
        :param status: Target status with availability and current queue time
        :type status: TargetStatus
        :return: Target instance
        :rtype: Target
        """
        if ".cpu" in status.id:
            platform = HardwarePlatform.CPU
        elif status.id.endswith("fpga"):
            platform = HardwarePlatform.FPGA
        else:
            raise ValueError(f"SimulatedAnnealing solver with name {status.id} is not supported.")

        return super().from_target_status(
            workspace=workspace,
            status=status,
            platform=platform,
            **kwargs
        )

    def supports_grouped_terms(self):
        if "legacy" in self.name or "fpga" in self.name:
            return False
        return True
    
    def supports_protobuf(self):
        if "legacy" in self.name or "fpga" in self.name:
            return False
        return True
