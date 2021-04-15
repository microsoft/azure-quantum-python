$PackageName = "azure-quantum-_client"
$PackageVersion = "0.0.1.0"
$Namespace = "azure.quantum._client"

$SpecsRepo = "https://github.com/Azure/azure-rest-api-specs.git"
$SpecsBranch = "master"
$SpecsCommitId = ""
$PathAllowList = ("specification/quantum")

$TempFolder = Join-Path $PSScriptRoot "../temp/"
$SpecsFolder = Join-Path $TempFolder  "/specs/"

$CheckoutScript = Join-Path $PSScriptRoot "./Checkout-Repo.ps1" -Resolve
# &$CheckoutScript -RepoUrl $SpecsRepo -TargetFolder $SpecsFolder -PathAllowList $PathAllowList -BranchName $SpecsBranch -CommitId $SpecsCommitId -Force | Write-Verbose

$TempGeneratedClientFolder = Join-Path $TempFolder "generated/_client/"
if (Test-Path $TempGeneratedClientFolder) {
    Remove-Item $TempGeneratedClientFolder -Recurse | Write-Verbose
}

$AutoRestConfig = Join-Path $SpecsFolder "specification/quantum/data-plane/readme.md" -Resolve

npm install -g autorest@latest | Write-Verbose

autorest $AutoRestConfig `
    --verbose `
    --python `
    --package-name=$PackageName `
    --package-version=$PackageVersion `
    --namespace=$Namespace `
    --no-namespace-folders=true `
    --add-credential `
    --python-mode=custom `
    --output-folder=$TempGeneratedClientFolder `
    | Write-Verbose

$AzureQuantumClient_Folder =  Join-Path $PSScriptRoot "../azure/quantum/_client/"
if (Test-Path $AzureQuantumClient_Folder) {
    Remove-Item $AzureQuantumClient_Folder -Recurse | Write-Verbose
}

Copy-Item $TempGeneratedClientFolder $AzureQuantumClient_Folder -Recurse -Force | Write-Verbose
