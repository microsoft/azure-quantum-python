#!/bin/env python
# -*- coding: utf-8 -*-
##
# setup.py: Installs QDK-Python: Python tools for the
# Microsoft Quantum Development Kit
##
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
##
import setuptools
import os

version = os.environ.get('PYTHON_VERSION', '0.0.0.1')
is_conda = bool(os.environ.get('CONDA_BUILD', False))

with open("./README.md", "r") as fh:
    long_description = fh.read()

import warnings
warnings.warn("The `qdk.chemistry` package is no longer maintained. " +
              "Please see the latest supported experiences for Azure Quantum here: "
              "https://learn.microsoft.com/azure/quantum/get-started-azure-quantum.",
              DeprecationWarning, stacklevel=2)

setuptools.setup(
    name="qdk",
    version=version,
    author="Microsoft",
    author_email="que-contacts@microsoft.com",
    description="Quantum Development Kit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/microsoft/qdk-python",
    packages=setuptools.find_namespace_packages(include=["qdk*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'qsharp',
        'jupyter_jsmol',
        'networkx',
        'varname',
        'ruamel-yaml',
        'basis_set_exchange',
        'jupyter_nbextensions_configurator',
        'pygments>=2.7.4',
        'ipython>=5.11.0',
        'ipywidgets==8.0.4' # version 8.0.5 causes JsmolView to break. See: https://github.com/fekad/jupyter-jsmol/issues/58
    ]
)