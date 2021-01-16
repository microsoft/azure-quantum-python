# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
Write-Host "##[info]Install package in development mode and run QDK-Pyton tests"
pip install -e .
pytest
