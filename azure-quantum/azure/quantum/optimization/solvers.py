##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging
import azure.quantum

from typing import List, Union, Any, Optional
from enum import Enum
from azure.quantum import Workspace, Job
from azure.quantum._client.models import JobDetails
from azure.quantum.optimization import Problem
from azure.quantum.storage import (
    ContainerClient,
    create_container_using_client,
)

logger = logging.getLogger(__name__)

__all__ = [
    "RangeSchedule",
    "Solver",
    "ParallelTempering",
    "SimulatedAnnealing",
    "HardwarePlatform",
    "Tabu",
    "QuantumMonteCarlo",
    "PopulationAnnealing",
    "SubstochasticMonteCarlo",
]


class RangeSchedule:
    def __init__(self, schedule_type: str, initial: float, final: float):
        """The constructor of Range Scheduler for solver.

        :param schedule_type:
            specifies schedule_type of range scheduler,
            currently only support 'linear' and 'geometric'.
        :param initial:
            initial value of range schedule.
        :param final:
            stop value of range schedule
        """
        self.schedule_type = schedule_type
        self.initial = initial
        self.final = final
        if not (
            self.schedule_type == "linear" or self.schedule_type == "geometric"
        ):
            raise ValueError(
                '"schedule_type" can only be "linear" or "geometric"!'
            )


class Solver:
    def __init__(
        self,
        workspace: Workspace,
        provider: str,
        target: str,
        input_data_format: str,
        output_data_format: str,
        nested_params: bool = True,
        force_str_params: bool = False,
    ):
        self.workspace = workspace
        self.target = target
        self.provider = provider
        self.input_data_format = input_data_format
        self.output_data_format = output_data_format
        self.nested_params = nested_params
        self.force_str_params = force_str_params
        self.params = {"params": {}} if nested_params else {}

    """Constants that define thresholds for submission warnings
    """
    SWEEPS_WARNING = 10000
    TIMEOUT_WARNING = 600

    def submit(
        self, problem: Union[str, Problem], compress: bool = True
    ) -> Job:
        """Submits a job to execution to the associated
        Azure Quantum Workspace.

        :param problem:
            The Problem to solve. It can be an instance of a Problem,
            or the URL of an Azure Storage Blob where the serialized version
            of a Problem has been uploaded.
        :param compress:
            Whether or not to compress the problem when uploading it
            the Blob Storage.
        """
        # Create a container URL:
        job_id = Job.create_job_id()
        logger.info(f"Submitting job with id: {job_id}")

        container_name = f"job-{job_id}"

        if not self.workspace.storage:
            # No storage account is passed, in this
            # case, get linked account from the service
            container_uri = self.workspace._get_linked_storage_sas_uri(
                container_name
            )
            container_client = ContainerClient.from_container_url(
                container_uri
            )
            create_container_using_client(container_client)
            container_uri = azure.quantum.storage.remove_sas_token(
                container_uri
            )
        else:
            # Storage account is passed, use it to generate a container_uri
            container_uri = azure.quantum.storage.get_container_uri(
                self.workspace.storage, container_name
            )

        logger.debug(f"Container URI: {container_uri}")

        if isinstance(problem, str):
            name = "Optimization problem"
            problem_uri = problem
        elif isinstance(problem, Problem):
            name = problem.name
            problem_uri = problem.upload(
                self.workspace,
                compress=compress,
                container_name=container_name,
                blob_name="inputData",
            )
        else:
            name = problem.name
            problem_uri = problem.uploaded_blob_uri

        logger.info(
            f"Submitting problem '{name}'. Using payload from: '{problem_uri}'"
        )

        details = JobDetails(
            id=job_id,
            name=name,
            container_uri=container_uri,
            input_data_format=self.input_data_format,
            output_data_format=self.output_data_format,
            input_data_uri=problem_uri,
            provider_id=self.provider,
            target=self.target,
            input_params=self.params,
        )

        logger.debug(f"==> submitting: {details}")
        job = self.workspace.submit_job(Job(self.workspace, details))
        return job

    def optimize(self, problem: Union[str, Problem]):
        """Submits the Problem to the associated
            Azure Quantum Workspace and get the results.

        :param problem:
            The Problem to solve. It can be an instance of a Problem,
            or the URL of an Azure Storage Blob where the serialized version
            of a Problem has been uploaded.
        """
        if not isinstance(problem, str):
            self.check_submission_warnings(problem)

        job = self.submit(problem)
        logger.info(f"Submitted job: '{job.id}'")

        return job.get_results()

    def set_one_param(self, name: str, value: Any):
        if value is not None:
            params = (
                self.params["params"] if self.nested_params else self.params
            )
            params[name] = str(value) if self.force_str_params else value

    def check_submission_warnings(self, problem: Problem):
        # print a warning if we suspect the job
        # may take long based on its configured properties.
        is_large_problem = problem.is_large()
        if is_large_problem:
            if self.nested_params and "sweeps" in self.params["params"]:
                sweeps = int(self.params["params"]["sweeps"])
                # if problem is large and sweeps is large, warn.
                if sweeps >= Solver.SWEEPS_WARNING:
                    logger.warning(
                        f"There is a large problem submitted and \
                        a large number of sweeps ({sweeps}) configured. \
                        This submission could result in a long runtime."
                    )

        # do a timeout check if param-free, to warn
        # new users who accidentally set high timeout values.
        if self.nested_params and "timeout" in self.params["params"]:
            timeout = int(self.params["params"]["timeout"])
            if timeout >= Solver.TIMEOUT_WARNING:
                logger.warning(
                    f"A large timeout has been set for this submission \
                        ({timeout}). \
                        If this is intended, disregard this warning. \
                        Otherwise, consider cancelling the job \
                        and resubmitting with a lower timeout."
                )

    def check_set_schedule(self, schedule: RangeSchedule, schedule_name: str):
        """Check whether the schedule parameter is set well from RangeSchedule.
        :param schedule:
            schedule paramter to be checked whether is from RangeSchedule.
        :param schedule_name:
            name of the schedule parameter.
        """
        if not (schedule is None):
            if not isinstance(schedule, RangeSchedule):
                raise ValueError(
                    f'{schedule_name} can only be from class "RangeSchedule"!'
                )
            schedule_param = {
                "type": schedule.schedule_type,
                "initial": schedule.initial,
                "final": schedule.final,
            }
            self.set_one_param(schedule_name, schedule_param)

    def check_set_positive_int(self, var: int, var_name: str):
        """Check whether the var parameter is a positive integer.
        :param var:
            var paramter to be checked whether is a positive integer.
        :param var_name:
            name of the variable.
        """
        if not (var is None):
            if not isinstance(var, int):
                raise ValueError(f"{var_name} shall be int!")
            if var <= 0:
                raise ValueError(f"{var_name} must be positive!")
            self.set_one_param(var_name, var)

    def check_set_float_limit(
        self, var: float, var_name: str, var_limit: float
    ):
        """Check whether the var parameter is a float larger than var_limit.
        :param var:
            var paramter to be checked
            whether is a float larger than var_limit.
        :param var_name:
            name of the variable.
        :var_limit:
            limit value of the variable to be checked.
        """
        if not (var is None):
            if not (isinstance(var, float) or isinstance(var, int)):
                raise ValueError(f"{var_name} shall be float!")
            if var <= var_limit:
                raise ValueError(
                    f"{var_name} can not be smaller than {var_limit}!"
                )
            self.set_one_param(var_name, var)


class HardwarePlatform(Enum):
    CPU = 1
    FPGA = 2


class ParallelTempering(Solver):
    def __init__(
        self,
        workspace: Workspace,
        sweeps: Optional[int] = None,
        replicas: Optional[int] = None,
        all_betas: Optional[List[int]] = None,
        timeout: Optional[int] = None,
        seed: Optional[int] = None,
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
            target = "microsoft.paralleltempering.fpga"
        else:
            target = (
                "microsoft.paralleltempering-parameterfree.cpu"
                if param_free
                else "microsoft.paralleltempering.cpu"
            )

        super().__init__(
            workspace=workspace,
            provider="Microsoft",
            target=target,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2",
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


class SimulatedAnnealing(Solver):
    def __init__(
        self,
        workspace: Workspace,
        beta_start: Optional[float] = None,
        beta_stop: Optional[float] = None,
        sweeps: Optional[int] = None,
        restarts: Optional[int] = None,
        timeout: Optional[int] = None,
        seed: Optional[int] = None,
        platform: Optional[HardwarePlatform] = HardwarePlatform.CPU,
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
            target = (
                "microsoft.simulatedannealing-parameterfree.fpga"
                if param_free
                else "microsoft.simulatedannealing.fpga"
            )
        else:
            target = (
                "microsoft.simulatedannealing-parameterfree.cpu"
                if param_free
                else "microsoft.simulatedannealing.cpu"
            )

        super().__init__(
            workspace=workspace,
            provider="Microsoft",
            target=target,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2",
        )

        self.set_one_param("beta_start", beta_start)
        self.set_one_param("beta_stop", beta_stop)
        self.set_one_param("sweeps", sweeps)
        self.set_one_param("restarts", restarts)
        self.set_one_param("timeout", timeout)
        self.set_one_param("seed", seed)


class Tabu(Solver):
    def __init__(
        self,
        workspace: Workspace,
        sweeps: Optional[int] = None,
        tabu_tenure: Optional[int] = None,
        timeout: Optional[int] = None,
        seed: Optional[int] = None,
        restarts: Optional[int] = None,
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
        param_free = (
            sweeps is None and tabu_tenure is None and restarts is None
        )

        target = (
            "microsoft.tabu-parameterfree.cpu"
            if param_free
            else "microsoft.tabu.cpu"
        )

        super().__init__(
            workspace=workspace,
            provider="Microsoft",
            target=target,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2",
        )

        self.set_one_param("sweeps", sweeps)
        self.set_one_param("tabu_tenure", tabu_tenure)
        self.set_one_param("timeout", timeout)
        self.set_one_param("seed", seed)
        self.set_one_param("restarts", restarts)


class QuantumMonteCarlo(Solver):
    def __init__(
        self,
        workspace: Workspace,
        trotter_number: Optional[int] = None,
        seed: Optional[int] = None,
        transverse_field_start: Optional[float] = None,
        transverse_field_stop: Optional[float] = None,
        restarts: Optional[int] = None,
        sweeps: Optional[int] = None,
        beta_start: Optional[float] = None,
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

        target = "microsoft.qmc.cpu"
        super().__init__(
            workspace=workspace,
            provider="Microsoft",
            target=target,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2",
        )
        self.set_one_param("sweeps", sweeps)
        self.set_one_param("trotter_number", trotter_number)
        self.set_one_param("seed", seed)
        self.set_one_param("transverse_field_start", transverse_field_start)
        self.set_one_param("transverse_field_stop", transverse_field_stop)
        self.set_one_param("beta_start", beta_start)
        self.set_one_param("restarts", restarts)


class PopulationAnnealing(Solver):
    def __init__(
        self,
        workspace: Workspace,
        alpha: Optional[float] = None,
        seed: Optional[int] = None,
        population: Optional[int] = None,
        sweeps: Optional[int] = None,
        beta: Optional[RangeSchedule] = None,
        culling_fraction: Optional[float] = None,
    ):
        """The constructor of Population Annealing Search solver.

        Population Annealing Search solver for binary optimization problems
        with k-local interactions on an all-to-all graph topology with double
        precision support for the coupler weights.

        This solver is CPU only, and not support parameter free now.

        :param alpha:
            ratio to trigger a restart, must be larger than 1
        :param seed:
            specifies a random seed value.
        :population:
            size of target population, must be positive
        :param sweeps:
            Number of monte carlo sweeps
        :param beta:
            beta value to control the annealing temperatures,
            it must be a object of RangeSchedule
        :param culling_fraction:
            constant culling rate, must be larger than 0
        """

        target = "microsoft.populationannealing.cpu"
        super().__init__(
            workspace=workspace,
            provider="Microsoft",
            target=target,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2",
        )

        self.check_set_float_limit(alpha, "alpha", 1.0)
        self.set_one_param("seed", seed)
        self.check_set_positive_int(population, "population")
        self.check_set_positive_int(sweeps, "sweeps")
        self.check_set_schedule(beta, "beta")
        self.check_set_float_limit(culling_fraction, "culling_fraction", 0.0)


class SubstochasticMonteCarlo(Solver):
    def __init__(
        self,
        workspace: Workspace,
        alpha: Optional[RangeSchedule] = None,
        seed: Optional[int] = None,
        target_population: Optional[int] = None,
        step_limit: Optional[int] = None,
        beta: Optional[RangeSchedule] = None,
        steps_per_walker: Optional[int] = None,
    ):
        """The constructor of Population Annealing Search solver.

        Population Annealing Search solver for binary optimization problems
        with k-local interactions on an all-to-all graph topology with double
        precision support for the coupler weights.

        This solver is CPU only, and not support parameter free now.

        :param alpha:
            alpha (chance to step) values evolve over time
        :param seed:
            specifies a random seed value.
        :target_population:
            size of target population, must be positive
        :param step_limit:
            number of monte carlo steps, must be positive
        :param beta:
            beta (resampling factor) values evolve over time
        :param steps_per_walker:
            number of steps to attempt for each walker, must be postive
        """
        target = "microsoft.substochasticmontecarlo.cpu"
        super().__init__(
            workspace=workspace,
            provider="Microsoft",
            target=target,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2",
        )
        self.set_one_param("seed", seed)
        self.check_set_schedule(beta, "beta")
        self.check_set_schedule(alpha, "alpha")
        self.check_set_positive_int(target_population, "target_population")
        self.check_set_positive_int(steps_per_walker, "steps_per_walker")
        self.check_set_positive_int(step_limit, "step_limit")
