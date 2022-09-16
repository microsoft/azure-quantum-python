#!/bin/env python
# -*- coding: utf-8 -*-
##
# setup.py: Installs Python host functionality for azure-quantum.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##

# IMPORTS #

import setuptools
import os
import distutils

# VERSION INFORMATION #
# Our build process sets the PYTHON_VERSION environment variable to a version
# string that is compatible with PEP 440, and so we inherit that version number
# here and propagate that to qsharp/version.py.
#
# To make sure that local builds still work without the same environment
# variables, we'll default to 0.0.0.1 as a development version.

version = os.environ.get("PYTHON_VERSION", "0.0.0.1")

with open("./azure/quantum/version.py", "w") as f:
    f.write(
        f"""# Auto-generated file, do not edit.
##
# version.py: Specifies the version of the azure.quantum package.
##
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
##
__version__ = "{version}"
"""
    )

with open("./azure/quantum/_client/_version.py", "w") as f:
    f.write(
        f"""# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

VERSION = "{version}"
"""
    )

# DESCRIPTION #
# The long description metadata passed to setuptools is used to populate the
# PyPI page for this package. Thus, we'll generate the description by using the
# same README.md file that we use in the GitHub repo.

with open("./README.md", "r") as fh:
    long_description = fh.read()

# LIST OF REQUIREMENTS #
# Get list of requirements from requirements.txt
with open("./requirements.txt", "r") as fh:
    requirements = fh.readlines()

# SETUPTOOLS INVOCATION #
setuptools.setup(
    name="azure-quantum",
    version=version,
    author="Microsoft",
    description="Python client for Azure Quantum",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/microsoft/qdk-python",
    packages=setuptools.find_namespace_packages(include=["azure.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    extras_require={
        "qiskit": [
            "qiskit-ionq>=0.3.3",
            "qiskit-terra>=0.19.1",
            "qiskit-qir>=0.1.0b12"
        ],
        "cirq": [
            "cirq-core==0.15.0",
            "cirq-ionq==1.0.0",
        ]
    }
)
