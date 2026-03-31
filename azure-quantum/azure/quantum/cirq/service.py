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
from azure.quantum.cirq.targets import *
from azure.quantum.cirq.targets.generic import AzureGenericQirCirqTarget
from azure.quantum.cirq.targets.target import Target as CirqTargetBase

from typing import Optional, Union, List, TYPE_CHECKING

if TYPE_CHECKING:
    from azure.quantum.cirq.targets import Target as CirqTarget
    from azure.quantum.cirq.job import Job as CirqJob
    from cirq_ionq import Job as CirqIonqJob

DEFAULT_JOB_NAME = "cirq-job"
CIRQ_USER_AGENT = "azure-quantum-cirq"


class AzureQuantumService:
    """
    Class for interfacing with the Azure Quantum service
    using Cirq quantum circuits
    """

    def __init__(
        self,
        workspace: Workspace = None,
        default_target: Optional[str] = None,
        **kwargs,
    ):
        """AzureQuantumService class

        :param workspace: Azure Quantum workspace. If missing it will create a new Workspace passing `kwargs` to the constructor. Defaults to None.
        :type workspace: Workspace
        :param default_target: Default target name, defaults to None
        :type default_target: Optional[str]
        """
        if kwargs is not None and len(kwargs) > 0:
            from warnings import warn

            warn(
                f"""Consider passing \"workspace\" argument explicitly. 
                 The ability to initialize AzureQuantumService with arguments {', '.join(f'"{argName}"' for argName in kwargs)} is going to be deprecated in future versions.""",
                DeprecationWarning,
                stacklevel=2,
            )

        if workspace is None:
            workspace = Workspace(**kwargs)

        workspace.append_user_agent(CIRQ_USER_AGENT)

        self._workspace = workspace
        self._default_target = default_target

    @property
    def _target_factory(self):
        from azure.quantum.target.target_factory import TargetFactory
        from azure.quantum.cirq.targets import Target, DEFAULT_TARGETS

        target_factory = TargetFactory(
            base_cls=Target, workspace=self._workspace, default_targets=DEFAULT_TARGETS
        )

        return target_factory

    def targets(
        self, name: str = None, provider_id: str = None, **kwargs
    ) -> Union["CirqTarget", List["CirqTarget"]]:
        """Get all quantum computing targets available in the Azure Quantum Workspace.

        :param name: Target name, defaults to None
        :type name: str
        :return: Target instance or list thereof
        :rtype: typing.Union[Target, typing.List[Target]]
        """

        target_statuses = self._workspace._get_target_status(name, provider_id)

        cirq_targets: List["CirqTarget"] = []
        for pid, status in target_statuses:
            target = self._target_factory.from_target_status(pid, status, **kwargs)

            if isinstance(target, CirqTargetBase):
                cirq_targets.append(target)
                continue

            # Pasqal uses a pulse-level input format (pasqal.pulser.v1) that is
            # incompatible with QIR submission. All other public Azure Quantum
            # targets are assumed to be QIR-compatible.
            _NON_QIR_PROVIDERS = {"pasqal"}
            if str(pid).strip().lower() in _NON_QIR_PROVIDERS:
                continue

            cirq_targets.append(
                AzureGenericQirCirqTarget.from_target_status(
                    self._workspace, pid, status, **kwargs
                )
            )

        # Back-compat with TargetFactory.get_targets return type.
        if name is not None:
            return cirq_targets[0] if cirq_targets else None
        return cirq_targets

    def get_target(self, name: str = None, **kwargs) -> "CirqTarget":
        """Get target with the specified name

        :param name: Target name
        :type name: str
        :return: Cirq target
        :rtype: Target
        """
        if name is None:
            if self._default_target is None:
                raise ValueError("No default target specified for job.")
            return self.targets(name=self._default_target, **kwargs)

        if isinstance(name, str):
            return self.targets(name=name, **kwargs)

    def get_job(self, job_id: str, *args, **kwargs) -> Union["CirqJob", "CirqIonqJob"]:
        """Get Cirq Job by job ID

        :param job_id: Job ID
        :type job_id: str
        :return: Job
        :rtype: azure.quantum.cirq.Job
        """
        job = self._workspace.get_job(job_id=job_id)
        # Recreate a Cirq-capable target wrapper for this job's target.
        target = self.targets(
            name=job.details.target, provider_id=job.details.provider_id
        )

        if target is None:
            raise RuntimeError(
                f"Job '{job_id}' exists, but no Cirq target wrapper could be created for target '{job.details.target}' (provider '{job.details.provider_id}'). "
                "AzureQuantumService.get_job only supports jobs submitted to Cirq-capable targets (provider-specific Cirq targets or the generic Cirq-to-QIR wrapper). "
                "For non-Cirq jobs, use Workspace.get_job(job_id)."
            )

        # Avoid misrepresenting arbitrary workspace jobs as Cirq jobs when using the
        # generic Cirq-to-QIR wrapper. The workspace target status APIs generally do
        # not expose supported input formats, so we rely on Cirq-stamped metadata.
        if isinstance(target, AzureGenericQirCirqTarget):
            metadata = job.details.metadata or {}
            cirq_flag = str(metadata.get("cirq", "")).strip().lower() == "true"
            if not cirq_flag:
                raise RuntimeError(
                    f"Job '{job_id}' targets '{job.details.target}' but does not appear to be a Cirq job. "
                    "Use Workspace.get_job(job_id) to work with this job."
                )

        try:
            return target._to_cirq_job(azure_job=job, *args, **kwargs)
        except Exception as exc:
            raise RuntimeError(
                f"Job '{job_id}' exists but could not be represented as a Cirq job for target '{job.details.target}' (provider '{job.details.provider_id}'). "
                "Use Workspace.get_job(job_id) to work with the raw job."
            ) from exc

    def create_job(
        self,
        program: cirq.Circuit,
        repetitions: int,
        name: str = DEFAULT_JOB_NAME,
        target: str = None,
        param_resolver: cirq.ParamResolverOrSimilarType = cirq.ParamResolver({}),
    ) -> Union["CirqJob", "CirqIonqJob"]:
        """Create job to run the given `cirq` program in Azure Quantum

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
        :rtype: azure.quantum.cirq.Job
        """
        # Get target
        _target = self.get_target(name=target)
        if not _target:
            # If the target exists in the workspace but was filtered out, provide
            # a more actionable error message.
            target_name = target or self._default_target
            ws_statuses = self._workspace._get_target_status(target_name)
            if ws_statuses:
                pid, status = ws_statuses[0]
                raise RuntimeError(
                    f"Target '{target_name}' exists in your workspace (provider '{pid}') and appears QIR-capable, but no Cirq-capable target could be created. "
                    "If you're using the generic Cirq-to-QIR path, ensure `qsharp` is installed: pip install azure-quantum[cirq,qsharp]."
                )

            raise RuntimeError(
                f"Could not find target '{target_name}'. "
                "Please make sure the target name is valid and that the associated provider is added to your Workspace. "
                "To add a provider to your quantum workspace on the Azure Portal, see https://aka.ms/AQ/Docs/AddProvider"
            )
        # Resolve parameters
        resolved_circuit = cirq.resolve_parameters(program, param_resolver)
        # Submit job to Azure
        return _target.submit(
            program=resolved_circuit, repetitions=repetitions, name=name
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
        """Run Cirq circuit on specified target, if target not specified then it runs on the default target

        :param program: Cirq program or circuit
        :type program: cirq.Circuit
        :param repetitions: Number of measurement repetitions
        :type repetitions: int
        :param target: Target name, defaults to default_target
        :type target: str
        :param name: Program name, defaults to "cirq-job"
        :type name: str
        :param param_resolver: Cirq parameters, defaults to `cirq.ParamResolver({})`
        :type param_resolver: cirq.ParamResolverOrSimilarType
        :param seed: Random seed for simulator results, defaults to None
        :type seed: cirq.RANDOM_STATE_OR_SEED_LIKE
        :param timeout_seconds: Timeout in seconds, defaults to None
        :type timeout_seconds: int
        :return: Measurement results
        :rtype: cirq.Result
        """
        job = self.create_job(
            program=program,
            repetitions=repetitions,
            name=name,
            target=target,
            param_resolver=param_resolver,
        )
        target_obj = self.get_target(name=target)

        # For SDK Cirq job wrappers, Job.results() already returns a Cirq result.
        from azure.quantum.cirq.job import Job as CirqJob
        if isinstance(job, CirqJob):
            return job.results(
                timeout_seconds=timeout_seconds,
                param_resolver=param_resolver,
                seed=seed,
            )

        # Otherwise, preserve provider-specific behavior (e.g., cirq_ionq.Job).
        try:
            result = job.results(timeout_seconds=timeout_seconds)
        except RuntimeError as e:
            # Catch errors from cirq_ionq.Job.results
            if "Job was not completed successful. Instead had status: " in str(e):
                raise TimeoutError(
                    f"The wait time has exceeded {timeout_seconds} seconds. \
Job status: '{job.status()}'."
                )
            else:
                raise e

        return target_obj._to_cirq_result(
            result=result,
            param_resolver=param_resolver,
            seed=seed,
        )
