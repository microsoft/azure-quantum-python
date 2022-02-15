# QIR pass-through

* Set your workspace details in the following environment variables:
  - `AZURE_QUANTUM_SUBSCRIPTION_ID `
  - `AZURE_QUANTUM_WORKSPACE_RG`
  - `AZURE_QUANTUM_WORKSPACE_NAME`
  - `AZURE_QUANTUM_WORKSPACE_LOCATION`

You can find the values for the above on the Overview panel in your Quantum Workspace in the Azure portal. To see which workspaces you can access, see https://aka.ms/aq/myworkspaces.
* To re-generate QIR file, simply run `dotnet build`
* To submit, install `azure-quantum`, then run `python .\submit.py`. 
