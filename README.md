# QDK-Python

## Introduction

QDK-Python is the repository for Python packages of the Quantum Development Kit (QDK). Currently, this consists of the following packages:

- qdk
- azure-quantum

Coming soom:

- qsharp

## Installation and getting started

To install the QDK package, we recommend installing the Anaconda Python distribution. For instructions on installing Conda on your system, please follow the [Conda user guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).

Currently, the QDK Python package is not yet released. When it is, it will be available via the `qdk` conda channel and can be installed as follows:

```bash
conda install -c qdk qdk
```

To get started running examples, start a Jupyter notebook:

```bash
cd examples
jupyter notebook
```

## Development

To create a new Conda environment, run:

```bash
conda env create -f environment.yml
```

Then to activate the environment:

```bash
conda activate qdk
```

To install the QDK package in development mode:

```bash
pip install -e qdk
```

## Contributing

This project welcomes contributions and suggestions.  Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft 
trademarks or logos is subject to and must follow 
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
