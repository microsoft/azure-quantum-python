##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging

from typing import List, Optional

from azure.quantum.target.solvers import HardwarePlatform, Solver
from azure.quantum.workspace import Workspace

logger = logging.getLogger(__name__)

class ParallelTempering(Solver):
    target_names = (
        "microsoft.paralleltempering.fpga",
        "microsoft.paralleltempering.cpu",
        "microsoft.paralleltempering-parameterfree.cpu",
    )
    def __init__(
        self,
        workspace: Workspace,
        name: str = "microsoft.paralleltempering.cpu",
        sweeps: Optional[int] = None,
        replicas: Optional[int] = None,
        all_betas: Optional[List[int]] = None,
        timeout: Optional[int] = None,
        seed: Optional[int] = None,
        **kwargs
    ):
        """The constructor of a Parallel Tempering solver.

        Multi-core Parallel Tempering solver for binary
        optimization problems with k-local interactions on an all-to-all
        graph topology with double precision support for the coupler weights.

        :param sweeps:
            specifies the number of sweeps.
        :param replicas:
            specifies the number of replicas.
        :param all_betas:
            a list of floats specifying the list of inverse temperatures.
            > Note: this list must be equal in
            length to the number of replicas.
        :param timeout:
            specifies maximum number of seconds to run the core solver
            loop. initialization time does not respect this value, so the
            solver may run longer than the value specified.
        :param seed:
            specifies a random seed value.
        """
        param_free = sweeps is None and replicas is None and all_betas is None
        platform = HardwarePlatform.CPU
        if platform == HardwarePlatform.FPGA:
            name = "microsoft.paralleltempering.fpga"
        elif param_free:
            name = "microsoft.paralleltempering-parameterfree.cpu"
 
        super().__init__(
            workspace=workspace,
            provider_id="Microsoft",
            name=name,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2",
            **kwargs
        )

        self.set_one_param("sweeps", sweeps)
        self.set_one_param("replicas", replicas)
        self.set_one_param("all_betas", all_betas)
        self.set_one_param("seed", seed)
        self.set_one_param("timeout", timeout)
        self.set_one_param("seed", seed)

        # Check parameters:
        if all_betas is not None:
            if replicas is None:
                self.set_one_param("replicas", len(all_betas))
            elif len(all_betas) != replicas:
                raise ValueError(
                    "Parameter 'replicas' must equal the"
                    + "length of the 'all_betas' parameters."
                )
