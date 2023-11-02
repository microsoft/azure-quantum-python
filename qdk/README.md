# qdk.chemistry

> [!WARNING]  
> This qdk.chemistry package is deprecated. Please see [Azure Quantum Elements](https://quantum.microsoft.com/our-story/quantum-elements-overview) for Azure Quantum's latest efforts in chemistry.

Q# chemistry library's Python application layer, contains tools for creating 2D molecular diagrams and calculating their 3D geometry using RDKit.

<img src="https://raw.githubusercontent.com/microsoft/qdk-python/main/qdk/caffeine.png" width=300 alt="Caffeine molecule">

### Installation and getting started

We recommend installing [Anaconda](https://www.anaconda.com/products/individual) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

First, install RDKit:

```bash
conda install -c conda-forge rdkit
```

To install the `qdk` package, run

```bash
pip install qdk
```

#### Development

To install the package in development mode, we recommend creating a new environment using the following command:

```bash
# Create new conda environment
conda env create -f qdk/environment.yml
```

Then, the package can be installed after activating the environment:

```bash
# Activate conda environment
conda activate qdk

# Install package in development mode
pip install -e qdk
```

