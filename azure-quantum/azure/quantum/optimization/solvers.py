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
        """Constructor of RangeSchedule for solvers.

        :param schedule_type:
            str, type of the RangeSchedule
            currently only supports 'linear' and 'geometric'.
        :param initial:
            float, initial value of RangeSchedule
        :param final:
            float, final value of the RangeSchedule
        """
        self.schedule_type = schedule_type
        self.initial = initial
        self.final = final
        if not (
            self.schedule_type == "linear" or self.schedule_type == "geometric"
        ):
            raise ValueError(
                '"schedule_type" must be "linear" or "geometric"!'
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

    def set_number_of_solutions(self, number_of_solutions: int):
        """Sets the number of solutions to return.

        Applies to all solvers.
        Default value is 1 if not supplied.

        :param number_of_solutions:
            Number of solutions to return. Must be a positive integer.
        """
        self.set_one_param("number_of_solutions", number_of_solutions)

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

    class ScheduleEvolution(Enum):
        INCREASING = 1
        DECREASING = 2

    def check_set_schedule(
        self,
        schedule_name: str,
        schedule_value: RangeSchedule,
        evolution: Optional[ScheduleEvolution] = None,
        lower_bound_exclusive: Optional[float] = None,
        lower_bound_inclusive: Optional[float] = None,
    ):
        """Set the parameter `schedule_name` from the value `schedule_value`
        and check that it is of type `RangeSchedule` and each end satisfies
        the specified bound.

        :param schedule_name:
            Name of the schedule parameter.
        :param schedule_value:
            Schedule value to be assigned and checked.
        :param evolution
            Expected schedule evolution (INCREASING or DECREASING)
        :lower_bound_exclusive:
            Exclusive lower bound for both ends of the schedule, optional.
        :lower_bound_inclusive:
            Inclusive lower bound for both ends of the schedule, optional.
        """
        if not (schedule_value is None):
            if not isinstance(schedule_value, RangeSchedule):
                raise ValueError(
                    f"{schedule_name} must be of type RangeSchedule; found"
                    f" type({schedule_name})={type(schedule_value).__name__}."
                )
            schedule_param = {
                "type": schedule_value.schedule_type,
                "initial": schedule_value.initial,
                "final": schedule_value.final,
            }
            if evolution is not None:
                if (evolution == self.ScheduleEvolution.INCREASING and
                        schedule_value.initial > schedule_value.final):
                    raise ValueError(
                            f"Schedule for {schedule_name} must be increasing;"
                            f" found {schedule_name}.initial"
                            f"={schedule_value.initial}"
                            f" > {schedule_value.final}"
                            f"={schedule_name}.final."
                    )
                if (evolution == self.ScheduleEvolution.DECREASING and
                        schedule_value.initial < schedule_value.final):
                    raise ValueError(
                            f"Schedule for {schedule_name} must be decreasing;"
                            f" found {schedule_name}.initial"
                            f"={schedule_value.initial}"
                            f" < {schedule_value.final}"
                            f"={schedule_name}.final."
                    )
            self.check_limit(
                    f"{schedule_name}.initial",
                    schedule_value.initial,
                    lower_bound_exclusive=lower_bound_exclusive,
                    lower_bound_inclusive=lower_bound_inclusive)
            self.check_limit(
                    f"{schedule_name}.final",
                    schedule_value.final,
                    lower_bound_exclusive=lower_bound_exclusive,
                    lower_bound_inclusive=lower_bound_inclusive)
            self.set_one_param(schedule_name, schedule_param)

    def check_set_positive_int(
            self,
            parameter_name: str,
            parameter_value: int):
        """Set the parameter `parameter_name` from the value `parameter_value`
        and check that it is a positive integer.

        :param parameter_name:
            Name of the parameter.
        :param parameter_value:
            Value to be assigned and checked.
        """
        if not (parameter_value is None):
            if not isinstance(parameter_value, int):
                raise ValueError(
                        f"{parameter_name} must be of type int; found"
                        f"type({parameter_name})"
                        f"={type(parameter_value).__name__}.")
            if parameter_value <= 0:
                raise ValueError(
                        f"{parameter_name} must be positive; found "
                        f"{parameter_name}={parameter_value}.")
            self.set_one_param(parameter_name, parameter_value)

    def check_set_float(
        self,
        parameter_name: str,
        parameter_value: float,
        lower_bound_exclusive: Optional[float] = None,
        lower_bound_inclusive: Optional[float] = None,
    ):
        """Set the parameter `parameter_name` from the value `parameter_value`
        and check that it has a float value satisfying bounds.

        :param parameter_name:
            Name of the parameter.
        :param parameter_value:
            Value to be assigned and checked.
        :lower_bound_exclusive:
            Exclusive lower bound to check parameter_value against, optional.
        :lower_bound_inclusive:
            Inclusive lower bound to check parameter_value against, optional.
        """
        if not (parameter_value is None):
            if not (isinstance(parameter_value, float) or
                    isinstance(parameter_value, int)):
                raise ValueError(f"{parameter_name} must be a float!")
            self.check_limit(
                    parameter_name=parameter_name,
                    parameter_value=parameter_value,
                    lower_bound_exclusive=lower_bound_exclusive,
                    lower_bound_inclusive=lower_bound_inclusive)
            self.set_one_param(parameter_name, parameter_value)

    def check_limit(
        self,
        parameter_name: str,
        parameter_value: Optional[float],
        lower_bound_exclusive: Optional[float] = None,
        lower_bound_inclusive: Optional[float] = None,
    ):
        """Check whether `parameter_value` satisfies a lower bound.

        :param parameter_name:
            Name of the parameter.
        :param parameter_value:
            Value to be checked.
        :lower_bound_exclusive:
            Exclusive lower bound to check parameter_value against, optional.
        :lower_bound_inclusive:
            Inclusive lower bound to check parameter_value against, optional.
        """
        if not (parameter_value is None):
            if (lower_bound_exclusive is not None and
                    parameter_value <= lower_bound_exclusive):
                raise ValueError(
                    f"{parameter_name} must be greater than "
                    f"{lower_bound_exclusive}; "
                    f"found {parameter_name}={parameter_value}."
                )
            if (lower_bound_inclusive is not None and
                    parameter_value < lower_bound_inclusive):
                raise ValueError(
                    f"{parameter_name} must be greater equal "
                    f"{lower_bound_inclusive}; found "
                    f"{parameter_name}={parameter_value}."
                )


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
        timeout: Optional[int] = None,
    ):
        """Constructor of the Population Annealing solver.

        Population Annealing Search solver for binary optimization problems
        with k-local interactions on an all-to-all graph topology with double
        precision support for the coupler weights.

        This solver is CPU only.
        It currently does not support parameter-free invocation.

        :param alpha:
            Ratio to trigger a restart. Must be larger than 1.
        :param seed:
            Specifies the random number generator seed value.
        :population:
            Size of the population. Must be positive.
        :param sweeps:
            Number of Monte Carlo sweeps. Must be positive.
        :param beta:
            Evolution of the inverse annealing temperature.
            Must be an object of type RangeSchedule describing
            an increasing evolution (0 < initial < final).
        :param timeout:
            specifies maximum number of seconds to run the core solver
            loop. initialization time does not respect this value, so the
            solver may run longer than the value specified. Setting this value
            will trigger the parameter free population annealing solver.
        """

        if timeout is None:
            target = "microsoft.populationannealing.cpu" 
        else:
            target = "microsoft.populationannealing-parameterfree.cpu"
        super().__init__(
            workspace=workspace,
            provider="Microsoft",
            target=target,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2",
        )

        self.check_set_float("alpha", alpha, lower_bound_exclusive=1.0)
        self.set_one_param("seed", seed)
        self.check_set_positive_int("population", population)
        self.check_set_positive_int("sweeps", sweeps)
        self.check_set_schedule(
                "beta", beta, evolution=self.ScheduleEvolution.INCREASING,
                lower_bound_exclusive=0)
        self.check_set_positive_int("timeout", timeout)


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
        timeout: Optional[int] = None,
    ):
        """Constructor of Substochastic Monte Carlo solver.

        Substochastic Monte Carlo solver for binary optimization problems
        with k-local interactions on an all-to-all graph topology with double
        precision support for the coupler weights.

        This solver is CPU only.
        It currently does not support parameter-free invocation.

        :param alpha:
            Evolution of alpha (chance to step) over time.
            Must be an object of type RangeSchedule describing a
            decreasing probability (1 >= initial > final >= 0).
        :param seed:
            Specifies the random number generator seed value.
        :target_population:
            Target size of the population. Must be positive.
        :param step_limit:
            Number of Monte Carlo steps (not sweeps!). Must be positive.
        :param beta:
            Evolution of beta (resampling factor) over time.
            Must be an object of type RangeSchedule describing
            an increasing evolution (0 < initial < final)
        :param steps_per_walker:
            Number of steps to attempt for each walker. Must be positive.
        :param timeout:
            Specifies maximum number of seconds to run the core solver
            loop. Initialization time does not respect this value, so the
            solver may run longer than the value specified. Setting this value
            will trigger the parameter free substochastic monte carlo solver.
        """

        if timeout is None:
            target = "microsoft.substochasticmontecarlo.cpu"
        else:
            target = "microsoft.substochasticmontecarlo-parameterfree.cpu"
        super().__init__(
            workspace=workspace,
            provider="Microsoft",
            target=target,
            input_data_format="microsoft.qio.v2",
            output_data_format="microsoft.qio-results.v2",
        )
        self.set_one_param("seed", seed)
        self.check_set_positive_int("steps_per_walker", steps_per_walker)
        self.check_set_positive_int("target_population", target_population)
        self.check_set_positive_int("step_limit", step_limit)
        self.check_set_schedule(
                "alpha", alpha, evolution=self.ScheduleEvolution.DECREASING,
                lower_bound_inclusive=0)
        self.check_set_schedule(
                "beta", beta, evolution=self.ScheduleEvolution.INCREASING,
                lower_bound_exclusive=0)
        self.check_set_positive_int("timeout", timeout)
