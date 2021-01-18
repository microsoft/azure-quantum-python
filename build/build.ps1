# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
Write-Host "##[info]Build QDK-Python package Conda environment"

# Create conda environment
conda env create --quiet --file environment.yml
