# Python SDK for Azure Quantum #

The `azure-quantum` package for Python provides functionality for interacting with Azure Quantum workspaces,
including creating jobs, listing jobs, and retrieving job results.

For details on how to get started with Azure Quantum, please visit https://azure.com/quantum.

You can also try our [Quantum Computing Fundamentals](https://aka.ms/learnqc) learning path to get familiar with the basic concepts of quantum computing, build quantum programs, and identify the kind of problems that can be solved.

## Installing with pip ##

```bash
pip install azure-quantum
```

## Development ##

The best way to install all the Python pre-reqs packages is to create a new Conda environment.
Run at the root of the `azure-quantum` directory:

```bash
conda env create -f environment.yml
```

Then to activate the environment:

```bash
conda activate azure-quantum
```

In case you have created the conda environment a while ago, you can make sure you have the latest versions of all dependencies by updating your environment:

```bash
conda env update -f environment.yml --prune
```

### Install the local development package ###

To install the package in development mode, run:

```bash
pip install -e .
```

### Unit tests ###

To run the unit tests, simply run `pytest` from the root of the `azure-quantum` directory:

```bash
pytest
```

To run the a specific unit test class, run:

```bash
pytest ./tests/unit/test_job.py
```

To run the a specific unit test case, run:

```bash
pytest -k test_job_refresh
```

## Building the `azure-quantum` Package ##

The Azure Quantum Python SDK uses a standard `setuptools`-based packaging strategy.
To build a platform-independent wheel, run the setup script with `bdist_wheel` instead:

```bash
cd src/Python/
python setup.py bdist_wheel
```

By default, this will create a `azure-quantum` wheel in `dist/` with the version number set to 0.0.0.1.
To provide a more useful version number, set the `PYTHON_VERSION` environment variable before running `setup.py`.

## Support and Q&A ##

If you have questions about the Quantum Development Kit and the Q# language, or if you encounter issues while using any of the components of the kit, you can reach out to the quantum team and the community of users in [Stack Overflow](https://stackoverflow.com/questions/tagged/q%23) and in [Quantum Computing Stack Exchange](https://quantumcomputing.stackexchange.com/questions/tagged/q%23) tagging your questions with **q#**.
