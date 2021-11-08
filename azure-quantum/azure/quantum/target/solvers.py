##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import logging

from typing import TYPE_CHECKING, Union, Any, Optional
from enum import Enum
from azure.quantum import Workspace, Job
from azure.quantum.job.base_job import DEFAULT_TIMEOUT
from azure.quantum.target.target import Target

if TYPE_CHECKING:
    from azure.quantum.optimization.problem import Problem

logger = logging.getLogger(__name__)

__all__ = [
    "HardwarePlatform",
    "RangeSchedule",
    "Solver",
]


class HardwarePlatform(Enum):
    CPU = 1
    FPGA = 2


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

proto_valid_solver_names = [
    "PopulationAnnealing",
    "SubstochasticMonteCarlo"
]

class Solver(Target):
    def __init__(
        self,
        workspace: Workspace,
        name: str,
        provider_id: str = "Microsoft",
        input_data_format="microsoft.qio.v2",
        output_data_format="microsoft.qio-results.v2",
        nested_params: bool = True,
        force_str_params: bool = False,
        params: dict = None,
        **kwargs
    ):
        self.provider_id = provider_id
        self.nested_params = nested_params
        self.force_str_params = force_str_params
        self.params = {"params": {}} if nested_params else {}
        params = params or {}
        name = self._switch_name(name, **params)

        super().__init__(
            workspace=workspace,
            name=name,
            input_data_format=input_data_format,
            output_data_format=output_data_format,
            provider_id=provider_id,
            content_type="application/json",
            encoding="gzip",
            **kwargs
        )
 
        self._set_params(**params)
        self._check_params(**params)


    """Constants that define thresholds for submission warnings
    """
    SWEEPS_WARNING = 10000
    TIMEOUT_WARNING = 600

    def _switch_name(self, name, **params):
        return name

    def _check_params(self, **params):
        pass

    @staticmethod
    def _encode_input_data(data: "Problem") -> bytes:
        return data.to_blob(compress=True)

    def submit(
        self, problem: Union[str, "Problem"], compress: bool = True
    ) -> Job:
        """Submits a job to execution to the associated
        Azure Quantum Workspace.

        :param problem:
            The Problem to solve. It can be an instance of a Problem,
            or the URL of an Azure Storage Blob where the serialized version
            of a Problem has been uploaded.
        :param compress:
            Whether or not to compress the problem when uploading it
            the Blob Storage. This input param is not used and will be
            deprecated.
        """
        if compress == False:
            import warnings
            warnings.warn("The service no longer accepts payloads that \
are not compressed with gzip encoding. Ignoring compress flag.")

        from azure.quantum.optimization import Problem
        if isinstance(problem, Problem):
            self.check_valid_problem(problem)
            return super().submit(
                input_data=problem,
                name=problem.name,
                input_params=self.params,
                blob_name="inputData"
            )

        else:
            if hasattr(problem, "uploaded_blob_uri"):
                name = problem.name
                problem_uri = problem.uploaded_blob_uri

            elif isinstance(problem, str):
                name = "Optimization problem"
                problem_uri = problem
            
            else:
                raise ValueError("Cannot submit problem: should be of type str, Problem or have uploaded_blob_uri attribute.")

            # Create job from storage URI
            job = Job.from_storage_uri(
                workspace=self.workspace,
                name=name,
                target=self.name,
                input_data_uri=problem_uri,
                provider_id=self.provider_id,
                input_data_format=self.input_data_format,
                output_data_format=self.output_data_format,
                input_params=self.params
            )

        return job

    def optimize(self, problem: Union[str, "Problem"], timeout_secs: int=DEFAULT_TIMEOUT):
        """[Submits the Problem to the associated
            Azure Quantum Workspace and get the results.

        :param problem:
            The Problem to solve. It can be an instance of a Problem,
            or the URL of an Azure Storage Blob where the serialized version
            of a Problem has been uploaded.
        :type problem: Union[str, Problem]
        :param timeout_secs: Timeout in seconds, defaults to 300
        :type timeout_secs: int
        :return: Job results
        :rtype: dict
        """
        if not isinstance(problem, str):
            self.check_submission_warnings(problem)

        job = self.submit(problem)
        logger.info(f"Submitted job: '{job.id}'")

        return job.get_results(timeout_secs=timeout_secs)

    def set_one_param(self, name: str, value: Any):
        if value is not None:
            params = (
                self.params["params"] if self.nested_params else self.params
            )
            params[name] = str(value) if self.force_str_params else value

    def _set_params(self, **params):
        for param_name, param in params.items():
            self.set_one_param(param_name, param)

    def set_number_of_solutions(self, number_of_solutions: int):
        """Sets the number of solutions to return.

        Applies to all solvers.
        Default value is 1 if not supplied.

        :param number_of_solutions:
            Number of solutions to return. Must be a positive integer.
        """
        self.set_one_param("number_of_solutions", number_of_solutions)

    def check_submission_warnings(self, problem: "Problem"):
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

    def check_valid_problem(self, problem):
        # Evaluate Problem and Solver compatibility.
        from azure.quantum.optimization.problem import ProblemType
        if problem.problem_type in {ProblemType.pubo_grouped, ProblemType.ising_grouped}:
            if not self.supports_grouped_terms():
                raise ValueError(
                    f"Solver type is not compatible"
                    f"with problem type {problem.problem_type};"
                    f"Try PopulationAnnealing or SubstochasticMonteCarlo."
                )
        if problem.content_type == "application/x-protobuf":
            if not self.supports_protobuf() and self.name not in proto_valid_solver_names:
                raise ValueError(
                    f"Solver `{self.name} type is not compatible "
                    f"for serialization with protobuf; "
                    f"Try PopulationAnnealing or SubstochasticMonteCarlo."
                )

    def supports_grouped_terms(self):
        """
        Return whether or not the Solver class supported grouped terms in the cost function.
        This should be overridden by Solver subclasses which do support grouped terms.
        """
        return False
    
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
            else:
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
