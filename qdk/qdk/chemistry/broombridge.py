# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

##
# Module for loading and encoding Broombridge data
##
import logging
from qsharp.chemistry import load_broombridge, load_input_state, encode
from typing import List, Tuple

NumQubits = int
HamiltonianTermList = Tuple[List[Tuple[List[int], List[float]]]]
InputStateTerms = Tuple[int, List[Tuple[Tuple[float, float], List[int]]]]
EnergyOffset = float
JWEncodedData = Tuple[
    NumQubits,
    HamiltonianTermList,
    InputStateTerms,
    EnergyOffset
]

_log = logging.getLogger(__name__)


def load_and_encode(
    file_name: str,
    problem_description_index: int = 0,
    initial_state_label: str = None
) -> JWEncodedData:
    """Wrapper function for loading and encoding Broombridge file into
    JWEncodedData-compatible format.

    :param file_name: Broombridge file name
    :type file_name: str
    :param problem_description_index: Index of problem description to use,
        defaults to 0
    :type problem_description_index: int, optional
    :param initial_state_label: Label of initial state to use, defaults to
        first available label
    :type initial_state_label: str, optional
    """
    broombridge_data = load_broombridge(file_name)
    problem = broombridge_data.problem_description[problem_description_index]

    if initial_state_label is None:
        # Pick first in list
        initial_state_label = problem.initial_state_suggestions[0].get("Label")
        _log.info(f"Using initial state label: {initial_state_label}")

    input_state = load_input_state(file_name, initial_state_label)
    ferm_hamiltonian = problem.load_fermion_hamiltonian()
    (
        num_qubits,
        hamiltonian_term_list,
        input_state_terms,
        energy_offset
    ) = encode(ferm_hamiltonian, input_state)

    return (
        num_qubits,
        hamiltonian_term_list,
        input_state_terms,
        energy_offset
    )
