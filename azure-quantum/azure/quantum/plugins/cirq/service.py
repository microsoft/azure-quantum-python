##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import cirq

from azure.quantum import Workspace
from azure.quantum.plugins.cirq.targets import (
    IonQSimulatorTarget,
    IonQQPUTarget,
    HoneywellAPIValidatorTarget,
    HoneywellSimulatorTarget,
    HoneywellQPUTarget,
)


class AzureQuantumService:
    """
    Class for interfacing with the Azure Quantum service
    using Cirq quantum circuits
    """
    def __init__(
        self,
        workspace: Workspace = None,
        default_target: str = None,
        **kwargs
    ):
        if workspace is None:
            kwargs.setdefault('user_agent', 'azure-quantum-cirq')
            workspace = Workspace(**kwargs)
        self._workspace = workspace
        self._default_target = default_target
        self._init_target_cls()
    
    def _init_target_cls(self):
        all_target_cls = [
            IonQSimulatorTarget,
            IonQQPUTarget,
            HoneywellAPIValidatorTarget,
            HoneywellSimulatorTarget,
            HoneywellQPUTarget,
        ]

        targets = [target.name for target in self._workspace.get_targets()]
        self._target_cls = {
            cls.target_name: cls for cls in all_target_cls if cls.target_name in targets
        }
    
    def targets(self, name: str = None, **kwargs):
        if not self._target_cls:
            self._init_target_cls()

        if not name:
            return [cls(self._workspace, **kwargs) for cls in self._target_cls]
        
        cls = self._target_cls.get(name)
        if cls is not None:
            return cls(self._workspace, **kwargs)
    
    def get_target(self, name: str = None, **kwargs):
        """Get target with the specified name"""
        return self.targets(name=name, **kwargs)

    def run(self, circuit: cirq.Circuit, repetitions: int, target: str = None):
        """Run Cirq circuit on specified target, if target not specified run on default target"""
        if target is None:
            target = self._default_target

        target = self.get_target(name=target)
        return target.submit(circuit=circuit, repetitions=repetitions)
