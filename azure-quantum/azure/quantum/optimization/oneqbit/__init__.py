# coding=utf-8
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
import warnings
warnings.warn("The azure.quantum.optimization.oneqbit namespace will be deprecated. \
Please use azure.quantum.target.oneqbit instead.")

from .solvers import (
    TabuSearch,
    PticmSolver,
    PathRelinkingSolver,
)
