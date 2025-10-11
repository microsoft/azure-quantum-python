# Development Setup

For developers who want to contribute to this package or run tests locally, follow these steps:

## Prerequisites

- Python 3.9 or later
- Git
- Powershell

## Setting up the development environment

1. Clone the repository:
   ```bash
   git clone https://github.com/microsoft/azure-quantum-python.git
   cd azure-quantum-python/azure-quantum
   ```
   In some cases you will need to "fork" the GitHub repository first.

1. Set up a virtual environment and install development dependencies:
   ```powershell
   # On Windows (PowerShell)
   .\eng\Setup-Dev-Env.ps1
   ```

1. (Optional) Install additional provider dependencies:
   ```bash
   # For specific providers
   pip install -e .[pulser,quil]
   
   # For all providers (requires Rust toolchain for PyQuil)
   pip install -e .[all]
   ```

## Running Tests

The development environment includes pytest for running unit tests. See [README](./azure-quantum/tests/README.md) for detailed testing instructions.

To run the unit tests, run `pytest` from the root of the `azure-quantum` directory:

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

### Recordings

To read more about how to create and update recordings for testing code that interacts with a live API, see the [README](./azure-quantum/tests/README.md).

Before merging your code contribution to `main`, make sure that all new code is covered by unit tests and that the unit tests have up-to-date recordings. If you recorded your tests and then updated or refactored the code, remember to re-record the tests.

## Building the `azure-quantum` Package wheel

The Azure Quantum Python SDK uses a standard `setuptools`-based packaging strategy.
To build a platform-independent wheel, run the setup script with `bdist_wheel` instead:

```bash
python setup.py bdist_wheel
```

By default, this will create a `azure-quantum` wheel in `dist/` with the version number set to 0.0.1.
To provide a more useful version number, set the `PYTHON_VERSION` environment variable before running `setup.py`.

## Update/re-generate the Azure Quantum internal SDK client

The internal Azure Quantum Python SDK client (`azure/quantum/_client`) needs to be re-generated every time there is a change in the [Azure Quantum Service API definition](https://github.com/Azure/azure-rest-api-specs/tree/main/specification/quantum/data-plane) (aka Swagger).

### Prerequisites
- Python 3.8 (or later)
- NodeJS 18.3 LTS (or later)

### Setup your repo
- Fork and clone the [azure-sdk-for-python](https://github.com/Azure/azure-sdk-for-python) repo (we call it SDK repo and it's absolute path)
- Create a branch in SDK repo to work in

Make sure your TypeSpec definition is merged into `main` branch of [Azure REST API Specs](https://github.com/Azure/azure-rest-api-specs) repo (we call it REST repo) or you already made a PR in REST repo so that you could get the GitHub link of your TypeSpec definition which contains commit ID (e.g. https://github.com/Azure/azure-rest-api-specs/blob/46ca83821edd120552403d4d11cf1dd22360c0b5/specification/contosowidgetmanager/Contoso.WidgetManager/tspconfig.yaml)

### Project service name and package name
Two key pieces of information for your project are the `service_name` and `package_name`.

The `service_name` is the short name for the Azure service. The `service_name` should match across all the SDK language repos and should be the name of the directory in the specification folder of the [Azure REST API Specs](https://github.com/Azure/azure-rest-api-specs) repo that contains the REST API definition file. An example is Service Bus, whose API definitions are in the `specification/servicebus` [folder](https://github.com/Azure/azure-rest-api-specs/tree/main/specification/servicebus), and uses the `service_name` - "servicebus". Not every service follows this convention, but it should be the standard unless there are strong reasons to deviate.

In Python, a project's package name is the name used to publish the package in PyPI. For data plane libraries (management plane uses a different convention), the `package_name` could be just `azure-{service_name}`. An example is "azure-servicebus".

Some services may need several different packages. For these cases a third component, the `module_name`, is added to the `package_name`, as `azure-{service_name}-{module_name}`. The `module_name` usually comes from the name of the REST API file itself or one of the directories toward the end of the file path. An example is the Synapse service, with packages "azure-synapse", "azure-synapse-accesscontrol", "azure-synapse-artifacts", etc.

### Project folder structure
Before we start, we probably should get to know the project folder for SDK repo.

Normally, the folder structure would be something like:

- `sdk/{service_name}/{package_name}` - the PROJECT_ROOT folder
- `/azure/{service_name}/{module_name}` - folder where generated code is.
- `/tests` - folder of test files
- `/samples` - folder of sample files
- `azure-{service_name}-{module_name}` - package name.

Usually, package name is same with part of `${PROJECT_ROOT}` folder. After release, you can find it in PyPi.   
For example: you can find "azure-messaging-webpubsubservice" in PyPi. There are also some other files (like `setup.py`, `README.md`, etc.) which are necessary for a complete package.
More details on the structure of Azure SDK repos is available in the Azure SDK common repo.

### How to generate SDK code with DataPlane Codegen
We are planning to automatically generate everything, but currently we still need some manual work to get a release-ready package. 

Here're the steps of how to get the package:
1. Configure python emitter in `tspconfig.yaml`
In rest repo, there shall be `tspconfig.yaml` where main.tsp of your service is. Make sure there are configuration for Python SDK like:
    ```yaml
    parameters:
      "service-dir":
        default: "YOUR_SERVICE_DIRECTORY"

    emit: [
      "@azure-tools/typespec-autorest", // this value does not affect python code generation
    ]

    options:
      "@azure-tools/typespec-python":
        package-dir: "YOUR_PACKAGE_NAME"
        package-name: "{package-dir}"
        flavor: "azure"
    ```
    `YOUR_PACKAGE_NAME` is your package name; `YOUR_SERVICE_DIRECTORY` is SDK directory name.   
    For example, assume that package name is "azure-ai-anomalydetector" and you want to put it in folder "azure-sdk-for-python/sdk/anomalydetector", then `YOUR_PACKAGE_NAME` is "azure-ai-anomalydetector" and `YOUR_SERVICE_DIRECTORY` is "sdk/anomalydetector"

2. Run cmd to generate the SDK
    Install tsp-client CLI tool:
    ```bash
    npm install -g @azure-tools/typespec-client-generator-cli
    ```
    For initial set up, from the root of the SDK repo, call:
    ```bash
    tsp-client init -c YOUR_REMOTE_TSPCONFIG_URL
    ```
    An example of `YOUR_REMOTE_TSPCONFIG_URL` is https://github.com/Azure/azure-rest-api-specs/blob/46ca83821edd120552403d4d11cf1dd22360c0b5/specification/contosowidgetmanager/Contoso.WidgetManager/tspconfig.yaml

To update your TypeSpec generated SDK, go to your SDK folder where your `tsp-location.yaml` is located, call:
```bash
tox run -e generate -c ..\..\..\eng\tox\tox.ini --root .
```
Note: To know more about `tox`, read our contributing guidelines

The `tox run -e generate` call will look for a `tsp-location.yaml` file in your local directory. `tsp-location.yaml` contains the configuration information that will be used to sync your TypeSpec project and generate your SDK. Please make sure that the commit is targeting the correct TypeSpec project updates you wish to generate your SDK from.

### After re-generating the client make sure to:

1. Re-run/Re-record all unit tests against the live-service (you can run [Record-Tests.ps1](./azure-quantum/eng/Record-Tests.ps1))
1. If necessary, adjust the convenience layer for breaking-changes or to expose new features
1. Add new unit-tests for new features and record them too

## Environment Variables ###

In addition to the [common Azure SDK environment variables](https://azure.github.io/azure-sdk/general_azurecore.html#environment-variables), you can also set the following environment variables to change the behaviour of the Azure Quantum SDK for Python:
| Environment Variable             | Description                                                            |
| -------------------------------- | ---------------------------------------------------------------------- |
| AZURE_QUANTUM_PYTHON_APPID       | Prefixes the HTTP User-Agent header with the specified value           |

## Code of Conduct ##

This project's code of conduct can be found in the
[here](./CODE_OF_CONDUCT.md).
