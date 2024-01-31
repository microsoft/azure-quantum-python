---
page_type: sample
author: guenp
description: Variational Quantum Eigensolver
ms.author: guenp@microsoft.com
ms.date: 05/02/2022
languages:
- python
products:
- azure-quantum
---

# Estimating the ground state energy of hydrogen using variational quantum eigensolvers (VQE) on Azure Quantum

This sample shows how to estimate the ground state energy of hydrogen using the Azure Quantum service. In particular, this sample uses the implementation of the variational quantum eigensolver algorithm provided with Qiskit to estimate minimum energies. The sample demonstrates running this VQE implementation on various Azure Quantum backends.

## Manifest

- [VQE-qiskit-hydrogen-session.ipynb](https://github.com/microsoft/azure-quantum-python/blob/main/samples/vqe/VQE-qiskit-hydrogen-session.ipynb): Python + Qiskit notebook demonstrating using VQE on multiple backends using a session.
