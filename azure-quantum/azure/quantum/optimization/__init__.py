# coding=utf-8
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

import warnings
warnings.warn(
    "Deprecation warning: azure.quantum.optimization will be deprecated. \
Please use azure.quantum.target and azure.quantum.target.optimization instead.")

from azure.quantum.target.optimization.term import *
from azure.quantum.target.optimization.problem import *
from azure.quantum.target.optimization.solvers import *
from azure.quantum.target.optimization.streaming_problem import *
from azure.quantum.target.optimization.online_problem import *
