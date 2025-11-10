# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2018.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

# Copyright 2021 IonQ, Inc. (www.ionq.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This code is copied from:
# - <https://github.com/qiskit-community/qiskit-ionq/blob/cea8f9874b992f82a35648582c06958869370c69/qiskit_ionq/ionq_gates.py>
# to enable Qiskit 1 & 2 compatibility as the original package only
# supports Qiskit 1 OR 2 depending on the package version.
# Modified by Microsoft Corporation for Azure Quantum integration and BackendV2 support (2025-11-10).

from typing import Optional
import math
import numpy as np
from qiskit.circuit.gate import Gate
from qiskit.circuit.parameterexpression import ParameterValueType

class GPIGate(Gate):
    r"""Single-qubit GPI gate.
    **Circuit symbol:**
    .. parsed-literal::
             ┌───────┐
        q_0: ┤ GPI(φ)├
             └───────┘
    **Matrix Representation:**

    .. math::

       GPI(\phi) =
            \begin{pmatrix}
                0 & e^{-i*2*\pi*\phi} \\
                e^{i*2*\pi*\phi} & 0
            \end{pmatrix}
    """

    def __init__(self, phi: ParameterValueType, label: Optional[str] = None):
        """Create new GPI gate."""
        super().__init__("gpi", 1, [phi], label=label)

    def __array__(self, dtype=None, copy=None):
        """Return a numpy array for the GPI gate."""
        top = np.exp(-1j * 2 * math.pi * self.params[0])
        bottom = np.exp(1j * 2 * math.pi * self.params[0])
        arr = np.array([[0, top], [bottom, 0]])  # build without dtype first
        if dtype is not None:
            arr = arr.astype(dtype, copy=False)  # avoid unnecessary copy
        if copy is True:
            return arr.copy()
        return arr


class GPI2Gate(Gate):
    r"""Single-qubit GPI2 gate.
    **Circuit symbol:**
    .. parsed-literal::
             ┌───────┐
        q_0: ┤GPI2(φ)├
             └───────┘
    **Matrix Representation:**

    .. math::

        GPI2(\phi) =
            \frac{1}{\sqrt{2}}
            \begin{pmatrix}
                1 & -i*e^{-i*2*\pi*\phi} \\
                -i*e^{i*2*\pi*\phi} & 1
            \end{pmatrix}
    """

    def __init__(self, phi: ParameterValueType, label: Optional[str] = None):
        """Create new GPI2 gate."""
        super().__init__("gpi2", 1, [phi], label=label)

    def __array__(self, dtype=None, copy=None):
        """Return a numpy array for the GPI2 gate."""
        top = -1j * np.exp(-1j * self.params[0] * 2 * math.pi)
        bottom = -1j * np.exp(1j * self.params[0] * 2 * math.pi)
        arr = (1 / np.sqrt(2)) * np.array([[1, top], [bottom, 1]])
        if dtype is not None:
            arr = arr.astype(dtype, copy=False)
        if copy is True:
            return arr.copy()
        return arr


class MSGate(Gate):
    r"""Entangling 2-Qubit MS gate.
    **Circuit symbol:**
    .. parsed-literal::
              _______
        q_0: ┤       ├-
             |MS(ϴ,0)|
        q_1: ┤       ├-
             └───────┘
    **Matrix representation:**

    .. math::

       MS(\phi_0, \phi_1, \theta) =
            \begin{pmatrix}
                cos(\theta*\pi) & 0 & 0 & -i*e^{-i*2*\pi(\phi_0+\phi_1)}*sin(\theta*\pi) \\
                0 & cos(\theta*\pi) & -i*e^{i*2*\pi(\phi_0-\phi_1)}*sin(\theta*\pi) & 0 \\
                0 & -i*e^{-i*2*\pi(\phi_0-\phi_1)}*sin(\theta*\pi) & cos(\theta*\pi) & 0 \\
                -i*e^{i*2*\pi(\phi_0+\phi_1)}*sin(\theta*\pi) & 0 & 0 & cos(\theta*\pi)
            \end{pmatrix}
    """

    def __init__(
        self,
        phi0: ParameterValueType,
        phi1: ParameterValueType,
        theta: Optional[ParameterValueType] = 0.25,
        label: Optional[str] = None,
    ):
        """Create new MS gate."""
        super().__init__(
            "ms",
            2,
            [phi0, phi1, theta],
            label=label,
        )

    def __array__(self, dtype=None, copy=None):
        """Return a numpy array for the MS gate."""
        phi0, phi1, theta = self.params
        diag = np.cos(math.pi * theta)
        sin = np.sin(math.pi * theta)
        arr = np.array(
            [
                [diag, 0, 0, sin * -1j * np.exp(-1j * 2 * math.pi * (phi0 + phi1))],
                [0, diag, sin * -1j * np.exp(1j * 2 * math.pi * (phi0 - phi1)), 0],
                [0, sin * -1j * np.exp(-1j * 2 * math.pi * (phi0 - phi1)), diag, 0],
                [sin * -1j * np.exp(1j * 2 * math.pi * (phi0 + phi1)), 0, 0, diag],
            ]
        )
        if dtype is not None:
            arr = arr.astype(dtype, copy=False)
        if copy is True:
            return arr.copy()
        return arr
