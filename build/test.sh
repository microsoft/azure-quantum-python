#!/bin/bash
echo "Run tests for env '$1', pkg dir '$2'"
conda activate $1
pip install -e $2
pytest $2
