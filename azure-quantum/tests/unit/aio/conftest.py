import os
import sys

try:
    from common import QuantumTestBase
except ImportError:
    # Add tests path to Python PATH to be able to access common.py
    aio_tests_path, _ = os.path.split(__file__)
    tests_path, _ = os.path.split(aio_tests_path)
    sys.path.append(tests_path)
