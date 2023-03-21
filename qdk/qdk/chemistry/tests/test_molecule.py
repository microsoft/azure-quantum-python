# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import rdkit

from qdk.chemistry.geometry.geometry import Geometry
from qdk.chemistry.molecule import Molecule


def test_from_xyz(caffeine_xyz):
    caffeine = Molecule.from_xyz(caffeine_xyz)
    assert caffeine.xyz() == caffeine._xyz
    Geometry.from_xyz(caffeine._xyz)
    formatted_xyz = "\n".join(" ".join(
        line.rstrip("00").replace("0 ", " ").split()
    ) for line in caffeine._xyz.split("\n"))
    assert caffeine.geometry.to_xyz("Caffeine") == formatted_xyz


def test_mol(caffeine):
    assert type(caffeine.mol) == rdkit.Chem.rdchem.Mol
    assert caffeine.smiles == "[H]Cn1c(=O)c2c(ncn2C)n(C)c1=O"
    assert caffeine.num_electrons == 102
    assert caffeine.atoms == [1, 6, 7, 8]
    assert caffeine.num_orbitals("STO-3G") == 80


def test_create_input(caffeine, tmp_path, h2o_molecule, h2o_nw):
    path = h2o_molecule.create_input(
        molecule_name="H2O",
        file_name="h2o.nw",
        solver="NWChem",
        base_path=tmp_path,
        num_active_orbitals=2
    )
    assert os.path.isfile(path)
    with open(path, "r") as f:
        data_gen = f.read()
    with open(h2o_nw, "r") as f:
        data_nw = f.read()
    assert data_gen == data_nw
