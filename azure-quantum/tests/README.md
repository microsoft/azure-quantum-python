# Unit tests

## Environment Pre-reqs

Before running the unit tests, set up your development environment using the venv-based setup:

### On Windows (PowerShell):
```powershell
.\eng\Setup-Dev-Env.ps1
```

This will install the package with common optional dependencies (qiskit, cirq, qsharp). To install additional provider dependencies, run:
```powershell
./venv/Scripts/activate        # Activate the virtual environment first
pip install -e .[pulser,quil]   # for specific providers
pip install -e .[all]           # for all providers (requires Rust toolchain)
```

## Tests

To run the tests, simply run `pytest` from the root of the `azure-quantum` directory:

```bash
pytest
```

To run a specific test class, run `pytest [test_file.py]`.
Example:

```bash
pytest ./tests/unit/local/test_job_results.py
```

To run a specific test case, run `pytest -k [test_method_name]`.
Example:

```bash
pytest -k test_job_refresh
```

### Qiskit multi-version matrix

To run Qiskit tests against both supported majors, run the tox environments from the `azure-quantum` directory using `tox -e py{310,311,312,313}-qiskit{1,2}`, for example:

```bash
tox -e py311-qiskit1
tox -e py311-qiskit2
```

Each command provisions an isolated virtual environment with the correct Qiskit version and executes `tests/unit/local/test_qiskit_offline.py`.
