# Build pipeline

This folder contains the scripts and .yml configuration files for the CI/CD pipeline to build, test and pack the packages in this repo as part of the QDK release.

The following files will be run by the QDK end-to-end build:

- build.ps1
- test.ps1
- pack.ps1

Additionally, the folder contains the `build.yml` and `steps.yml` files that run the standalone pipeline for the Python packages. This consists of the following steps:

1. Create Conda environment using `environment.yml` file
2. Activate environment and run unit tests using `pytest`
3. Run Component Governance checks to make sure that the packages are compliant with CVE guidelines

The component governance checks are automated through Azure Devops and makes use of the open source [license curation](https://github.com/clearlydefined/curated-data) by clearlydefined.io.
