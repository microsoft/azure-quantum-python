##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging

from typing import Optional

from azure.quantum.target.solvers import Solver
from azure.quantum.workspace import Workspace

logger = logging.getLogger(__name__)

class QuantumMonteCarlo(Solver):
    target_names = (
        "microsoft.qmc.cpu",
    )
    def __init__(
        self,
        workspace: Workspace,
        name: str = "microsoft.qmc.cpu",
        trotter_number: Optional[int] = None,
        seed: Optional[int] = None,
        transverse_field_start: Optional[float] = None,
        transverse_field_stop: Optional[float] = None,
        restarts: Optional[int] = None,
        sweeps: Optional[int] = None,
        beta_start: Optional[float] = None,
        **kwargs
    ):
        """The constructor of Simulated Qunatum Annelaing Search solver.

        Simulated Quantum Search solver for binary optimization problems
        with k-local interactions on an all-to-all graph topology with double
        precision support for the coupler weights.

        This solver is CPU only.

        :param trotter_number:
            specifies the number of trotter time slices
            i.e. number of copies of each variable.
        :param seed:
            specifies a random seed value.
        :param sweeps:
            Number of monte carlo sweeps
        :param transverse_field_start:
            starting strength of the external field
        :param transverse_field_end:
            ending strength of the external field
        :param beta_start:
            Low starting temp i.e. beta start
        :param restarts:
            Number of simulation runs
        """

        super().__init__(
            workspace=workspace,
            provider_id="Microsoft",
            name=name,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2",
            **kwargs
        )
        self.set_one_param("sweeps", sweeps)
        self.set_one_param("trotter_number", trotter_number)
        self.set_one_param("seed", seed)
        self.set_one_param("transverse_field_start", transverse_field_start)
        self.set_one_param("transverse_field_stop", transverse_field_stop)
        self.set_one_param("beta_start", beta_start)
        self.set_one_param("restarts", restarts)
