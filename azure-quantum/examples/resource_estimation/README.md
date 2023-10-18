# Resource estimator examples

This directory contains several standalone Python scripts that use the Azure
Quantum Resource Estimator through the `azure_quantum` Python API.

## Example scripts

Some of the scripts require a resource id and a location, which can be obtained
from the _Overview_ page of your _Azure Quantum workspace_.

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
