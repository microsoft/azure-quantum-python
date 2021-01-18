# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
Write-Host "##[info]Build QDK-Python package Conda environment"

# Create conda environment
eval "$(conda shell.bash hook)"
conda env create --quiet --file environment.yml
