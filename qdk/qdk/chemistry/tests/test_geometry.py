# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
import pytest
from qdk.chemistry.geometry import Element, Geometry


def test_Element():
    c1 = Element(
        name="C",
        x=0.0,
        y=0.0,
        z=0.0
    )

    c2 = Element(
        name="C",
        x=1.0,
        y=0.0,
        z=0.0
    )

    g = Geometry([c1, c2])
    assert g[0] == c1
    assert g[1] == c2


@pytest.fixture
def xyz():
    return """3
water
O 0.002 0.398 0.0
H 0.762 -0.203 0.0
H -0.764 -0.195 0.0"""


def test_geometry_from_mol(h2o):
    g = Geometry.from_mol(h2o)
    assert g.charge == 0
    assert len(g) == 3
    assert [el.name for el in g] == ["O", "H", "H"]


def test_geometry_to_from_xyz(geometry, xyz):
    assert geometry.to_xyz("water") == xyz
    gprime = Geometry.from_xyz(xyz)
    assert geometry == gprime
