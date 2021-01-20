# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
from unittest import mock

import pytest
import ruamel.yaml as yaml

from qdk.chemistry.solvers.nwchem import create_input_deck, parse_nwchem_output


@pytest.fixture()
def test_deck():
    return """
start HHO_test

echo
memory stack 1000 mb heap 100 mb global 1000 mb noverify

geometry units au
symmetry c1
O 0.002 0.398 0.0
H 0.762 -0.203 0.0
H -0.764 -0.195 0.0
end

basis
* library sto-3g
end



scf
thresh 1.0e-08
tol2e 1e-09
singlet
rhf
maxiter 200

end

tce
ccsd
2eorb
2emet 13
tilesize 20

thresh 1.0e-08
end

set tce:print_integrals T
set tce:qorb 7
set tce:qela 3
set tce:qelb 3

task tce energy
"""


def test_nwchem(geometry, h2o, test_deck):
    mol_name = "HHO_test"
    with mock.patch("qdk.chemistry.geometry.Geometry.from_mol") as _m:
        _m.return_value = geometry

        nw_chem_input = create_input_deck(
            mol=h2o,
            mol_name=mol_name,
            num_active_orbitals=7
        )

    assert nw_chem_input == test_deck


def test_nwchem_pass_geometry(geometry, h2o, test_deck):
    mol_name = "HHO_test"
    nw_chem_input = create_input_deck(
        mol_name=mol_name,
        geometry=geometry,
        num_active_orbitals=7,
        mol=h2o
    )

    assert nw_chem_input == test_deck


def test_parse_nwchem_output(caffeine_nw, caffeine_output):
    assert parse_nwchem_output(caffeine_nw, caffeine_output) == {
        'number of atoms': 24,
        'number of orbitals': 80,
        'SCF energy': -627.628748906485,
        'CCSD correlation energy': -0.002197738334726,
        'geometry snapshot': []
    }
