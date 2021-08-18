##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
from typing import Dict, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from azure.quantum.target import Target
    from azure.quantum import Workspace


def get_all_targets() -> Dict[str, "Target"]:
    """Get all target classes by provider ID"""
    from azure.quantum.target import IonQ, Honeywell
    from azure.quantum.target.optimization import Solver

    class MicrosoftOptimization(Solver):
        """Microsoft Optimization Solver.
        Initializes a default solver for a given target name.
        """
        def __init__(
            self,
            workspace: "Workspace",
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
            from azure.quantum.target.optimization import (
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


    return {
        "ionq": IonQ,
        "honeywell": Honeywell,
        "Microsoft": MicrosoftOptimization
    }


class TargetFactory:
    def __init__(self, workspace: "Workspace"):
        self.workspace = workspace

    
    def _target_cls(self, name: str):
        pass

    def from_target_status(self, *target_statuses, **kwargs):
        all_targets = get_all_targets()
        targets = [
            all_targets.get(_provider_id).from_target_status(self.workspace, status, **kwargs)
            for _provider_id, status in target_statuses
            if _provider_id in all_targets
        ]
        targets = [t for t in targets if t is not None]
        if len(targets) == 1:
            return targets[0]
        return targets
