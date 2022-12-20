![Azure Quantum logo](https://raw.githubusercontent.com/microsoft/qdk-python/main/azure-quantum/Azure-Quantum-logo.png)

# Azure Quantum #

[![Build Status](https://dev.azure.com/ms-quantum-public/Microsoft%20Quantum%20(public)/_apis/build/status/microsoft.qdk-python?branchName=main)](https://dev.azure.com/ms-quantum-public/Microsoft%20Quantum%20(public)/_build/latest?definitionId=32&branchName=main) [![PyPI version](https://badge.fury.io/py/azure-quantum.svg)](https://badge.fury.io/py/azure-quantum)

Azure Quantum is Microsoft's cloud service for running Quantum Computing circuits or solving Optimization problems with our quantum partners and technologies. The `azure-quantum` package for Python provides functionality for interacting with Azure Quantum workspaces,
including creating jobs, listing jobs, and retrieving job results. For more information, view the [Azure Quantum Documentation](https://docs.microsoft.com/azure/quantum).

This package supports submitting quantum circuits or problem definitions written with Python. To submit quantum programs written with Q#, Microsoft's Domain-specific language for Quantum Programming, view [Submit Q# Jobs to Azure Quantum](https://docs.microsoft.com/azure/quantum/how-to-submit-jobs).

## Installation ##

The package is released on PyPI and can be installed via `pip`:

```bash
pip install azure-quantum
```

To use `azure-quantum` for submitting quantum circuits expressed with [Qiskit](https://pypi.org/project/qiskit), install with optional dependencies:

```bash
pip install azure-quantum[qiskit]
```

To use `azure-quantum` for submitting quantum circuits expressed with [Cirq](https://pypi.org/project/cirq), install with optional dependencies:

```bash
pip install azure-quantum[cirq]
```

## Getting started and Quickstart guides ##

To work in Azure Quantum, you need an Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/). Follow the [Create an Azure Quantum workspace](https://docs.microsoft.com/azure/quantum/how-to-create-workspace) how-to guide to set up your Workspace and enable your preferred providers.

To get started, visit the following Quickstart guides:

- [Quickstart: Submit a circuit with Qiskit](https://docs.microsoft.com/azure/quantum/quickstart-microsoft-qiskit)
- [Quickstart: Submit a circuit with Cirq](https://docs.microsoft.com/azure/quantum/quickstart-microsoft-qiskit)
- [Quickstart: Submit a circuit with a provider-specific format](https://docs.microsoft.com/azure/quantum/quickstart-microsoft-provider-format).
- [Quickstart: Solve a simple optimization problem](https://docs.microsoft.com/azure/quantum/quickstart-microsoft-qio?pivots=platform-microsoft#express-a-simple-problem).

## General usage ##

To connect to your Azure Quantum Workspace, go to the [Azure Portal](https://portal.azure.com), navigate to your Workspace and copy-paste the resource ID and location into the code snippet below.

```python
from azure.quantum import Workspace

# Enter your Workspace details (resource ID and location) below
workspace = Workspace(
    resource_id="",
    location=""
)
```

### List all targets ###

To list all targets that are available to your workspace, run

```python
workspace.get_targets()
```

### Submit a quantum circuit or optimization problem ###

First, define a quantum circuit or optimization problem, and create a job by submitting it to one of the available targets:

```python
# Enter target name below
target = workspace.get_targets("")

# Submit quantum circuit or optimization problem
job = target.submit(problem)

# Wait for job to complete and fetch results
result = job.get_results()
```

## Contributing ##

For details on contributing to this repository, see the [contributing guide](https://github.com/microsoft/qdk-python/blob/main/CONTRIBUTING.md).

This project welcomes contributions and suggestions. Most contributions require you to agree to a Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us the rights to use your contribution. For details, visit
https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions provided by the bot. You will only need to do this once across all repositories using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/)
or contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Support ##

If you run into any problems or bugs using this package, please head over to the [issues](https://github.com/microsoft/qdk-python/issues) page and open a new issue, if it does not already exist.
