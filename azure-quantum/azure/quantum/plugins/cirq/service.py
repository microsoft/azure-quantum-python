##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
try:
    import cirq
except ImportError:
    raise ImportError(
    "Missing optional 'cirq' dependencies. \
To install run: pip install azure-quantum[cirq]"
)

from azure.quantum import Workspace
from azure.quantum.job.base_job import DEFAULT_TIMEOUT
from azure.quantum.plugins.cirq.targets import *

from typing import Optional, Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    import cirq_ionq
    from azure.quantum.plugins.cirq.targets import Target as CirqTarget
    from azure.quantum.target import Target
    from azure.quantum.plugins.cirq.job import Job as CirqJob

DEFAULT_JOB_NAME = "cirq-job"


class AzureQuantumService:
    """
    Class for interfacing with the Azure Quantum service
    using Cirq quantum circuits
    """
    def __init__(
        self,
        workspace: Workspace = None,
        default_target: Optional[str] = None,
        **kwargs
    ):
        """AzureQuantumService class

        :param workspace: Azure Quantum workspace, defaults to None
        :type workspace: Workspace, optional
        :param default_target: Default target name, defaults to None
        :type default_target: Optional[str], optional
        """
        if workspace is None:
            workspace = Workspace(**kwargs)

        self._workspace = workspace
        self._workspace.user_agent = kwargs.pop("user-agent", "azure-quantum-cirq")
        self._default_target = default_target

    def targets(
        self,
        name: str = None,
        provider_id: str = None,
        **kwargs
    ) -> Union["CirqTarget", List["CirqTarget"]]:
        """Get all targets available in the Azure Quantum.

        :param name: Target name, defaults to None
        :type name: str, optional
        :return: Target instance or list thereof
        :rtype: Union[Target, List[Target]]
        """
        from azure.quantum.target.target_factory import TargetFactory
        from azure.quantum.plugins.cirq.targets import Target, DEFAULT_TARGETS

        target_factory = TargetFactory(
            base_cls=Target,
            workspace=self._workspace,
            default_targets=DEFAULT_TARGETS
        )

        return target_factory.get_targets(
            name=name,
            provider_id=provider_id
        )

    def get_target(self, name: str = None, **kwargs) -> "CirqTarget":
        """Get target with the specified name

        :param name: Target name
        :type name: str
        :return: Cirq target
        :rtype: CirqTarget
        """
        return self.targets(name=name, **kwargs)

    def create_job(
        self,
        program: cirq.Circuit,
        repetitions: int,
        name: str = DEFAULT_JOB_NAME,
        target: str = None,
        param_resolver: cirq.ParamResolverOrSimilarType = cirq.ParamResolver({})
    ) -> Union["CirqJob", "cirq_ionq.Job"]:
        """Create job using a Cirq program

        :param program: Cirq program or circuit
        :type program: cirq.Circuit
        :param repetitions: Number of measurements 
        :type repetitions: int
        :param name: Program name
        :type name: str
        :param target: Target name
        :type target: str
        :param param_resolver: Parameter resolver for cirq program
        :type param_resolver: cirq.ParamResolverOrSimilarType
        :return: Job
        :rtype: azure.quantum.plugins.cirq.Job
        """
        # Get target
        if target is None:
            if self._default_target is None:
                raise ValueError("No default target specified for job.")
            target = self._default_target
        if isinstance(target, str):
            target = self.get_target(name=target)
        # Resolve parameters
        resolved_circuit = cirq.resolve_parameters(program, param_resolver)
        # Submit job to Azure
        return target.submit(
            program=resolved_circuit,
            repetitions=repetitions,
            name=name
        )

    def run(
        self,
        program: cirq.Circuit,
        repetitions: int,
        target: str = None,
        name: str = DEFAULT_JOB_NAME,
        param_resolver: cirq.ParamResolverOrSimilarType = cirq.ParamResolver({}),
        seed: cirq.RANDOM_STATE_OR_SEED_LIKE = None,
        timeout_seconds: int = DEFAULT_TIMEOUT,
    ) -> cirq.Result:
        """Run Cirq circuit on specified target, if target not specified run on default target

        :param program: Cirq program or circuit
        :type program: cirq.Circuit
        :param repetitions: Number of measurement repetitions
        :type repetitions: int
        :param target: Target name, defaults to default_target
        :type target: str, optional
        :param name: Program name, defaults to "cirq-job"
        :type name: str, optional
        :param param_resolver: Cirq parameters, defaults to cirq.ParamResolver({})
        :type param_resolver: cirq.ParamResolverOrSimilarType, optional
        :param seed: Random seed for simulator results, defaults to None
        :type seed: cirq.RANDOM_STATE_OR_SEED_LIKE, optional
        :param timeout_seconds: Timeout in seconds, defaults to None
        :type timeout_seconds: int, optional
        :return: Measurement results
        :rtype: cirq.Result
        """
        # Get target
        if target is None:
            if self._default_target is None:
                raise ValueError("No default target specified for job.")
            target = self._default_target
        target = self.get_target(name=target)
        job = self.create_job(
            program=program,
            repetitions=repetitions,
            name=name,
            target=target,
            param_resolver=param_resolver
        )
        # Get raw job results
        result = job.results(timeout_seconds=timeout_seconds)

        # Convert to Cirq Result
        return target._to_cirq_result(
            result=result,
            param_resolver=param_resolver,
            seed=seed
        )
