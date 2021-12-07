import os 
import pytest

@pytest.fixture()
def script_path():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, "..", "..", "..", "examples", "estimate-job-cost")


def test_estimate_scripts(script_path):
    for file_name in [
        "estimate_honeywell.py",
        "estimate_ionq.py"
    ]:
        file_path = os.path.join(script_path, file_name)
        exec(open(file_path).read())
