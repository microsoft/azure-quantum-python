##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional, Type
from ...job import Job
from ...job.base_job import ContentType
from ...workspace import Workspace
from ..params import InputParams, InputParamsItem, AutoValidatingParams, \
    validating_field
from ..target import Target
from . import MicrosoftEstimatorJob


@dataclass
class MicrosoftEstimatorQubitParams(AutoValidatingParams):
    @staticmethod
    def check_instruction_set(name, value):
        if value not in ["gate-based", "gate_based", "GateBased", "gateBased",
                         "Majorana", "majorana"]:
            raise ValueError(f"{name} must be GateBased or Majorana")
        
    @staticmethod
    def check_time(name, value):
        pat = r"^(\+?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*(s|ms|μs|µs|us|ns)$"
        if re.match(pat, value) is None:
            raise ValueError(f"{name} is not a valid time string; use a "
                             "suffix s, ms, us, or ns")

    @staticmethod
    def check_error_rate(name, value):
        if value <= 0.0 or value >= 1.0:
            raise ValueError(f"{name} must be between 0 and 1")

    name: Optional[str] = None
    instruction_set: Optional[str] = validating_field(check_instruction_set)
    one_qubit_measurement_time: Optional[str] = validating_field(check_time)
    two_qubit_joint_measurement_time: Optional[str] = \
        validating_field(check_time)
    one_qubit_gate_time: Optional[str] = validating_field(check_time)
    two_qubit_gate_time: Optional[str] = validating_field(check_time)
    t_gate_time: Optional[str] = validating_field(check_time)
    one_qubit_measurement_error_rate: Optional[float] = \
        validating_field(check_error_rate)
    two_qubit_joint_measurement_error_rate: Optional[float] = \
        validating_field(check_error_rate)
    one_qubit_gate_error_rate: Optional[float] = \
        validating_field(check_error_rate)
    two_qubit_gate_error_rate: Optional[float] = \
        validating_field(check_error_rate)
    t_gate_error_rate: Optional[float] = validating_field(check_error_rate)

    _default_models = ["qubit_gate_us_e3", "qubit_gate_us_e4",
                       "qubit_gate_ns_e3", "qubit_gate_ns_e4",
                       "qubit_maj_ns_e4", "qubit_maj_ns_e6"]
    _gate_based = ["gate-based", "gate_based", "GateBased", "gateBased"]
    _maj_based = ["Majorana", "majorana"]

    def post_validation(self, result):
        # check whether all fields have been specified in case a custom qubit
        # model is specified
        custom = result != {} and \
            (self.name is None or self.name not in self._default_models)

        # no further validation needed for non-custom models
        if not custom:
            return

        # instruction set must be set
        if self.instruction_set is None:
            raise LookupError("instruction_set must be set for custom qubit "
                              "parameters")

        # NOTE at this point, we know that instruction set must have valid
        # value
        if self.one_qubit_measurement_time is None:
            raise LookupError("one_qubit_measurement_time must be set")
        if self.one_qubit_measurement_error_rate is None:
            raise LookupError("one_qubit_measurement_error_rate must be set")

        # this only needs to be checked for gate based qubits
        if self.instruction_set in self._gate_based:
            if self.one_qubit_gate_time is None:
                raise LookupError("one_qubit_gate_time must be set")

@dataclass
class MicrosoftEstimatorQecScheme(AutoValidatingParams):
    name: Optional[str] = None
    error_correction_threshold: Optional[float] = None
    crossing_prefactor: Optional[float] = None
    logical_cycle_time: Optional[str] = None
    physical_qubits_per_logical_qubit: Optional[str] = None


class MicrosoftEstimatorInputParamsItem(InputParamsItem):
    """
    Input params for microsoft.estimator target

    :ivar error_budget Total error budget for execution of the algorithm
    """

    def __init__(self):
        super().__init__()

        self.qubit_params: MicrosoftEstimatorQubitParams = \
            MicrosoftEstimatorQubitParams()
        self.qec_scheme: MicrosoftEstimatorQecScheme = \
            MicrosoftEstimatorQecScheme()
        self.error_budget: Optional[float] = None

    def as_dict(self, validate=True) -> Dict[str, Any]:
        result = super().as_dict(validate)

        qubit_params = self.qubit_params.as_dict(validate)
        if len(qubit_params) != 0:
            result["qubitParams"] = qubit_params

        qec_scheme = self.qec_scheme.as_dict(validate)
        if len(qec_scheme) != 0:
            result["qecScheme"] = qec_scheme

        if self.error_budget is not None:
            if validate and (self.error_budget <= 0 or self.error_budget >= 1):
                raise ValueError("error_budget must be value between 0 and 1")
            result["errorBudget"] = self.error_budget

        return result


class MicrosoftEstimatorParams(InputParams, MicrosoftEstimatorInputParamsItem):
    def __init__(self, num_items: Optional[int] = None):
        InputParams.__init__(
            self,
            num_items=num_items,
            item_type=MicrosoftEstimatorInputParamsItem)


class MicrosoftEstimator(Target):
    """
    Resource estimator target from the microsoft-qc provider.
    """

    target_names = [
        "microsoft.estimator"
    ]

    def __init__(
        self,
        workspace: "Workspace",
        name: str = "microsoft.estimator",
        **kwargs
    ):
        # There is only a single target name for this target
        assert name == self.target_names[0]

        # make sure to not pass argument twice
        kwargs.pop("provider_id", None)

        super().__init__(
            workspace=workspace,
            name=name,
            input_data_format="qir.v1",
            output_data_format="microsoft.resource-estimates.v1",
            provider_id="microsoft-qc",
            content_type=ContentType.json,
            **kwargs
        )

    @classmethod
    def _get_job_class(cls) -> Type[Job]:
        return MicrosoftEstimatorJob
    
    def _qir_output_data_format(self) -> str:
        """"Fallback output data format in case of QIR job submission."""
        return "microsoft.resource-estimates.v1"

    def make_params(self, num_items: Optional[int] = None):
        return MicrosoftEstimatorParams(num_items=num_items)
