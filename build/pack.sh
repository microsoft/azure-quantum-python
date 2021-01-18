#!/bin/bash
echo "Pack wheel for env '$1'"
eval "$(conda shell.bash hook)"
conda activate $1
which python
pwd
python setup.py bdist_wheel sdist --formats=gztar
