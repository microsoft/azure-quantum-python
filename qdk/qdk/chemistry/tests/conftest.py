# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
import pytest
import os

from rdkit.Chem import AllChem as Chem

from qdk.chemistry.geometry import Geometry, Element
from qdk.chemistry.molecule import Molecule


@pytest.fixture()
def h2o():
    mol = Chem.AddHs(Chem.MolFromSmiles("O"))
    return mol


@pytest.fixture()
def geometry(h2o):
    el = [
        Element("O", 0.002, 0.398, 0.0),
        Element("H", 0.762, -0.203, 0.0),
        Element("H", -0.764, -0.195, 0.0)
    ]
    return Geometry(el, charge=Chem.GetFormalCharge(h2o))


@pytest.fixture()
def h2o_xyz():
    path, _ = os.path.split(__file__)
    return os.path.join(path, "data", "h2o.xyz")


@pytest.fixture()
def caffeine_xyz():
    path, _ = os.path.split(__file__)
    return os.path.join(path, "data", "caffeine.xyz")


@pytest.fixture()
def h2o_nw():
    path, _ = os.path.split(__file__)
    return os.path.join(path, "data", "h2o.nw")


@pytest.fixture()
def h2o_molecule(h2o_xyz):
    return Molecule.from_xyz(h2o_xyz)


@pytest.fixture()
def caffeine(caffeine_xyz):
    return Molecule.from_xyz(caffeine_xyz)


@pytest.fixture()
def caffeine_output():
    path, _ = os.path.split(__file__)
    return os.path.join(path, "data", "caffeine.output")


@pytest.fixture()
def caffeine_nw():
    path, _ = os.path.split(__file__)
    return os.path.join(path, "data", "caffeine.nw")
