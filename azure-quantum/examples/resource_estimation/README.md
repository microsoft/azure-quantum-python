# Resource estimator examples

This directory contains several standalone Python scripts that use the Azure
Quantum Resource Estimator through the `azure-quantum` Python API.

## Prerequisites

These scripts require access to an Azure Quantum workspace.  Read [our
documentation](https://learn.microsoft.com/azure/quantum/how-to-create-workspace?tabs=payg%2Ctabid-quick)
to learn how to set up an Azure Quantum workspace.  Once the Azure Quantum
workspace is created, you can retrieve the _resource id_ and _location_ from
the _Overview_ page of your workspace.

Also, you need to install the `azure-quantum` Python package:

```shell
python -m pip install azure-quantum
```

## Example scripts

* **[cli.py](https://github.com/microsoft/qdk-python/blob/main/azure-quantum/examples/resource_estimation/cli.py): A resource estimation CLI that can execute resource
  estimation jobs from various input formats and generate JSON output.**

  The input type is determined by file extension:

  * `.qs`: Q# snippet (without `namespace` declaration)
  * `.qasm`: OpenQASM file
  * `.ll`: QIR in ASCII format
  * `.qir`, `.bc`: QIR bitcode

  Usage:

  Resource estimation from an OpenQASM file:

  ```shell
  python cli.py -r "resource id" -l "location" cli_test_files/rqft_multiplier.qasm
  ```

  Resource estimation from a Q# file with job parameters:

  ```shell
  python cli.py -r "resource id" -l "location" cli_test_files/multiplier.qs \
      -p cli_test_files/multiplier.json
  ```

  Writing output into JSON file:

  ```shell
  python cli.py -r "resource id" -l "location" cli_test_files/multiplier.qs \
      -p cli_test_files/multiplier.json \
      -o output.json
  ```
