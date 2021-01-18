#!/bin/bash
echo "Run tests for env '$1', pkg dir '$2'"
eval "$(conda shell.bash hook)"
conda activate $1
which python
python -m pip install --upgrade pip
pip install pytest pytest-azurepipelines
pip install -e $2
pytest $2
