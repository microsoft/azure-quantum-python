##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import Union
from azure.quantum import Workspace
from azure.quantum.optimization.solvers import (
    Solver,
    ParallelTempering,
    SimulatedAnnealing,
    Tabu,
    QuantumMonteCarlo,
    PopulationAnnealing,
    SubstochasticMonteCarlo,
)

MICROSOFT_QIO_SOLVERS = {
    "microsoft.paralleltempering.cpu": ParallelTempering,
    "microsoft.simulatedannealing.cpu": SimulatedAnnealing,
    "microsoft.tabu.cpu": Tabu,
    "microsoft.qmc.cpu": QuantumMonteCarlo,
    "microsoft.populationannealing.cpu": PopulationAnnealing,
    "microsoft.substochasticmontecarlo.cpu": SubstochasticMonteCarlo,
    "microsoft.paralleltempering-parameterfree.cpu": None,
    "microsoft.simulatedannealing-parameterfree.cpu": None,
    "microsoft.tabu-parameterfree.cpu": None,
    "microsoft.qmc-parameterfree.cpu": None,
    "microsoft.populationannealing-parameterfree.cpu": None,
    "microsoft.substochasticmontecarlo-parameterfree.cpu": None,
}


class MicrosoftOptimization(Solver):
    """Microsoft Optimization Solver.
    Initializes a default solver for a given target name.
    """
    def __init__(
        self,
        workspace: Workspace,
        name: str,
        input_data_format="microsoft.qio.v2",
        output_data_format="microsoft.qio-results.v2",
        provider_id: str = "Microsoft",
        **kwargs
    ):
        super().__init__(
            workspace=workspace,
            name=name,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            provider_id=provider_id,
            **kwargs
        )

    @classmethod
    def from_target_status(
        cls, workspace, status, **kwargs
    ) -> Union["MicrosoftOptimization", Solver]:
        """Create a MicrosoftOptimization or Solver instance from a given workspace
        and target status.

        :param workspace: Associated workspace
        :type workspace: Workspace
        :param status: Target status with availability and current queue time
        :type status: TargetStatus
        :return: Target instance
        :rtype: MicrosoftOptimization
        """
        name = status.id
        if name in MICROSOFT_QIO_SOLVERS:
            cls = MICROSOFT_QIO_SOLVERS.get(name)
            if cls is not None:
                return cls.from_target_status(
                    workspace=workspace, status=status, **kwargs
                )
        else:
            return super().from_target_status(
                workspace=workspace, status=status, **kwargs
            )
