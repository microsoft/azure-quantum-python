##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import re
import warnings
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Type, Union, List

from ...job import Job
from ...job.base_job import ContentType
from ...workspace import Workspace
from ..params import InputParams, InputParamsItem, AutoValidatingParams, \
    validating_field
from ..target import Target
from . import MicrosoftEstimatorJob

class QubitParams:
    GATE_US_E3 = "qubit_gate_us_e3"
    GATE_US_E4 = "qubit_gate_us_e4"
    GATE_NS_E3 = "qubit_gate_ns_e3"
    GATE_NS_E4 = "qubit_gate_ns_e4"
    MAJ_NS_E4 = "qubit_maj_ns_e4"
    MAJ_NS_E6 = "qubit_maj_ns_e6"


class QECScheme:
    """
    Resource estimator QEC Scheme.
    """
    SURFACE_CODE = "surface_code"
    FLOQUET_CODE = "floquet_code"


def _check_error_rate(name, value):
    if value <= 0.0 or value >= 1.0:
        raise ValueError(f"{name} must be between 0 and 1")

def _check_error_rate_or_process_and_readout(name, value):
    if value is None:
        return

    if isinstance(value, float):
        _check_error_rate(name, value)
        return

    if not isinstance(value, MeasurementErrorRate):
        raise ValueError(f"{name} must be either a float or "
                         "MeasurementErrorRate with two fields: 'process' and 'readout'")

def check_time(name, value):
    pat = r"^(\+?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)\s*(s|ms|μs|µs|us|ns)$"
    if re.match(pat, value) is None:
        raise ValueError(f"{name} is not a valid time string; use a "
                         "suffix s, ms, us, or ns")

@dataclass
class MeasurementErrorRate(AutoValidatingParams):
    process: float = field(metadata={"validate": _check_error_rate})
    readout: float = field(metadata={"validate": _check_error_rate})

@dataclass
class MicrosoftEstimatorQubitParams(AutoValidatingParams):
    @staticmethod
    def check_instruction_set(name, value):
        if value not in ["gate-based", "gate_based", "GateBased", "gateBased",
                         "Majorana", "majorana"]:
            raise ValueError(f"{name} must be GateBased or Majorana")

    name: Optional[str] = None
    instruction_set: Optional[str] = validating_field(check_instruction_set)
    one_qubit_measurement_time: Optional[str] = validating_field(check_time)
    two_qubit_joint_measurement_time: Optional[str] = \
        validating_field(check_time)
    one_qubit_gate_time: Optional[str] = validating_field(check_time)
    two_qubit_gate_time: Optional[str] = validating_field(check_time)
    t_gate_time: Optional[str] = validating_field(check_time)
    one_qubit_measurement_error_rate: Union[None, float, MeasurementErrorRate] = \
        validating_field(_check_error_rate_or_process_and_readout)
    two_qubit_joint_measurement_error_rate: Union[None, float, MeasurementErrorRate] = \
        validating_field(_check_error_rate_or_process_and_readout)
    one_qubit_gate_error_rate: Optional[float] = \
        validating_field(_check_error_rate)
    two_qubit_gate_error_rate: Optional[float] = \
        validating_field(_check_error_rate)
    t_gate_error_rate: Optional[float] = validating_field(_check_error_rate)
    idle_error_rate: Optional[float] = validating_field(_check_error_rate)

    _default_models = [QubitParams.GATE_US_E3, QubitParams.GATE_US_E4,
                       QubitParams.GATE_NS_E3, QubitParams.GATE_NS_E4,
                       QubitParams.MAJ_NS_E4, QubitParams.MAJ_NS_E6]
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

    def as_dict(self, validate=True) -> Dict[str, Any]:
        qubit_params = super().as_dict(validate)
        if len(qubit_params) != 0:
            if isinstance(self.one_qubit_measurement_error_rate, MeasurementErrorRate):
                qubit_params["oneQubitMeasurementErrorRate"] = \
                self.one_qubit_measurement_error_rate.as_dict(validate)

            if isinstance(self.two_qubit_joint_measurement_error_rate, MeasurementErrorRate):
                qubit_params["twoQubitJointMeasurementErrorRate"] = \
                self.two_qubit_joint_measurement_error_rate.as_dict(validate)

        return qubit_params


@dataclass
class MicrosoftEstimatorQecScheme(AutoValidatingParams):
    name: Optional[str] = None
    error_correction_threshold: Optional[float] = \
        validating_field(_check_error_rate)
    crossing_prefactor: Optional[float] = None
    logical_cycle_time: Optional[str] = None
    physical_qubits_per_logical_qubit: Optional[str] = None


@dataclass
class ProtocolSpecificDistillationUnitSpecification(AutoValidatingParams):
    num_unit_qubits: Optional[int] = None
    duration_in_qubit_cycle_time: Optional[int] = None

    def post_validation(self, result):
        if self.num_unit_qubits is None:
            raise LookupError("num_unit_qubits must be set")

        if self.duration_in_qubit_cycle_time is None:
            raise LookupError("duration_in_qubit_cycle_time must be set")


@dataclass
class DistillationUnitSpecification(AutoValidatingParams):
    name: Optional[str] = None
    display_name: Optional[str] = None
    num_input_ts: Optional[int] = None
    num_output_ts: Optional[int] = None
    failure_probability_formula:  Optional[str] = None
    output_error_rate_formula:  Optional[str] = None
    physical_qubit_specification: Optional[ProtocolSpecificDistillationUnitSpecification] = None
    logical_qubit_specification: Optional[ProtocolSpecificDistillationUnitSpecification] = None
    logical_qubit_specification_first_round_override: \
        Optional[ProtocolSpecificDistillationUnitSpecification] = None

    def has_custom_specification(self):
        return \
        self.display_name is not None \
        or self.num_input_ts is not None \
        or self.num_output_ts is not None \
        or self.failure_probability_formula is not None \
        or self.output_error_rate_formula is not None \
        or self.physical_qubit_specification is not None \
        or self.logical_qubit_specification is not None \
        or self.logical_qubit_specification_first_round_override is not None

    def has_predefined_name(self):
        return self.name is not None

    def post_validation(self, result):
        if not self.has_custom_specification() and not self.has_predefined_name():
            raise LookupError("name must be set or custom specification must be provided")

        if self.has_custom_specification() and self.has_predefined_name():
            raise LookupError("If predefined name is provided, "
                            "custom specification is not allowed. "
                            "Either remove name or remove all other "
                            "specification of the distillation unit")

        if self.has_predefined_name():
            return # all other validation is on the server side

        if self.num_input_ts is None:
            raise LookupError("num_input_ts must be set")

        if self.num_output_ts is None:
            raise LookupError("num_output_ts must be set")

        if self.failure_probability_formula is None:
            raise LookupError("failure_probability_formula must be set")

        if self.output_error_rate_formula is None:
            raise LookupError("output_error_rate_formula must be set")

        if self.physical_qubit_specification is not None:
            self.physical_qubit_specification.post_validation(result)

        if self.logical_qubit_specification is not None:
            self.logical_qubit_specification.post_validation(result)

        if self.logical_qubit_specification_first_round_override is not None:
            self.logical_qubit_specification_first_round_override.post_validation(result)

    def as_dict(self, validate=True) -> Dict[str, Any]:
        specification_dict = super().as_dict(validate)
        if len(specification_dict) != 0:
            if self.physical_qubit_specification is not None:
                physical_qubit_specification_dict = \
                self.physical_qubit_specification.as_dict(validate)
                if len(physical_qubit_specification_dict) != 0:
                    specification_dict["physicalQubitSpecification"] = \
                        physical_qubit_specification_dict

            if self.logical_qubit_specification is not None:
                logical_qubit_specification_dict = \
                self.logical_qubit_specification.as_dict(validate)
                if len(logical_qubit_specification_dict) != 0:
                    specification_dict["logicalQubitSpecification"] = \
                        logical_qubit_specification_dict

            if self.logical_qubit_specification_first_round_override is not None:
                logical_qubit_specification_first_round_override_dict = \
                self.logical_qubit_specification_first_round_override.as_dict(validate)
                if len(logical_qubit_specification_first_round_override_dict) != 0:
                    specification_dict["logicalQubitSpecificationFirstRoundOverride"] = \
                        logical_qubit_specification_first_round_override_dict

        return specification_dict


@dataclass
class ErrorBudgetPartition(AutoValidatingParams):
    """
    Resource estimator error budget partition parameters.
    """
    logical: float = 0.001 / 3
    t_states: float = 0.001 / 3
    rotations: float = 0.001 / 3


@dataclass
class MicrosoftEstimatorConstraints(AutoValidatingParams):
    """
    Resource estimator constraints.
    """

    @staticmethod
    def at_least_one(name, value):
        if value < 1:
            raise ValueError(f"{name} must be at least 1")

    logical_depth_factor: Optional[float] = validating_field(at_least_one)
    max_t_factories: Optional[int] = validating_field(at_least_one)
    max_duration: Optional[int] = validating_field(check_time)
    max_physical_qubits: Optional[int] = validating_field(at_least_one)

    def post_validation(self, result):
        if self.max_duration is not None and self.max_physical_qubits is not None:
            raise LookupError("Both duration and number of physical qubits constraints are provided, but only one is allowe at a time.")


@dataclass
class MicrosoftEstimatorProfiling(AutoValidatingParams):
    @staticmethod
    def at_most_30(name, value):
        if value < 0 or value > 30:
            raise ValueError(f"{name} must be nonnegative and at most 30")

    call_stack_depth: Optional[int] = validating_field(at_most_30)
    inline_functions: Optional[bool] = None


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
        self.distillation_unit_specifications = []  # type: List[DistillationUnitSpecification]
        self.constraints: MicrosoftEstimatorConstraints = \
            MicrosoftEstimatorConstraints()
        self.profiling: MicrosoftEstimatorProfiling = \
            MicrosoftEstimatorProfiling()
        self.error_budget: Optional[Union[float, ErrorBudgetPartition]] = None

    def as_dict(self, validate=True) -> Dict[str, Any]:
        result = super().as_dict(validate)

        qubit_params = self.qubit_params.as_dict(validate)
        if len(qubit_params) != 0:
            result["qubitParams"] = qubit_params

        qec_scheme = self.qec_scheme.as_dict(validate)
        if len(qec_scheme) != 0:
            result["qecScheme"] = qec_scheme

        for specification in self.distillation_unit_specifications:
            specification_dict = specification.as_dict(validate)
            if len(specification_dict) != 0:
                if result.get("distillationUnitSpecifications") is None:
                    result["distillationUnitSpecifications"] = []

                result["distillationUnitSpecifications"].append(specification_dict)

        constraints = self.constraints.as_dict(validate)
        if len(constraints) != 0:
            result["constraints"] = constraints

        profiling = self.profiling.as_dict(validate)
        if len(profiling) != 0:
            result["profiling"] = profiling

        if self.error_budget is not None:
            if isinstance(self.error_budget, float) or \
                    isinstance(self.error_budget, int):
                if validate and \
                        (self.error_budget <= 0 or self.error_budget >= 1):
                    message = "error_budget must be value between 0 and 1"
                    raise ValueError(message)
                result["errorBudget"] = self.error_budget
            elif isinstance(self.error_budget, ErrorBudgetPartition):
                result["errorBudget"] = self.error_budget.as_dict(validate)

        return result


class MicrosoftEstimatorParams(InputParams, MicrosoftEstimatorInputParamsItem):
    """
    Resource estimator input parameters.
    """
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

    def submit(
        self,
        input_data: Any,
        name: str = "azure-quantum-job",
        shots: int = None,
        input_params: Union[Dict[str, Any], InputParams, None] = None,
        **kwargs,
    ) -> Job:
        """
        Submit an estimation job.

        :param input_data: Input data
        :type input_data: Any
        :param name: Job name
        :type name: str
        :param shots: Number of shots. Ignored in estimation. Defaults to None
        :type shots: int
        :param input_params: Input parameters
        :type input_params: Dict[str, Any]
        :return: Azure Quantum job
        :rtype: Job
        """

        if shots is not None:
            warnings.warn("The 'shots' parameter is ignored in resource estimation job.")

        try:
            from qiskit import QuantumCircuit, transpile
            from qiskit_qir import to_qir_module
            from qiskit_qir.visitor import SUPPORTED_INSTRUCTIONS
            if isinstance(input_data, QuantumCircuit):
                input_data = transpile(input_data,
                                       basis_gates=SUPPORTED_INSTRUCTIONS,
                                       optimization_level=0)
                (module, _) = to_qir_module(input_data, record_output=False)
                input_data = module.bitcode
        finally:
            return super().submit(
                input_data=input_data, 
                name=name, 
                shots=shots,
                input_params=input_params, 
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
