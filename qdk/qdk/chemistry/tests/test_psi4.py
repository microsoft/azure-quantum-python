# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
import pytest
from unittest import mock

from qdk.chemistry.solvers.psi4 import create_input_deck


@pytest.fixture()
def test_deck():
    return """
memory 1 GB

molecule  {
symmetry C1
0 1
  None
}

set {
  basis 3-21G
  scf_type PK
  reference rhf
  d_convergence 1e-8
  e_convergence 1e-8
}


e, wfn = energy('SCF', return_wfn=True)
e = energy('HF')
fcidump(wfn, fname='fcidump', oe_ints=['EIGENVALUES'])
clean()

"""


def test_psi4(geometry, h2o, test_deck):
    with mock.patch("qdk.chemistry.geometry.Geometry.from_mol") as _m:
        _m.return_value = geometry

        psi4_input = create_input_deck(
            mol=h2o,
            method="HF",
            driver="energy"
        )

    assert psi4_input == test_deck
