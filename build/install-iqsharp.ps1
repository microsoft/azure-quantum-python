<#
    .SYNOPSIS
        Installs prerequisites needed for testing the submiting 
        Q#/QIR jobs generated with IQ# (job submission via the Azure Quantum Python SDK).

        It will first check if we are on a multi-repository build which contains the
        build's IQ# Nuget package and Python wheel in the drop folder. 
        If they exist, then we will install them.       
        Otherwise, this is (likely) a standalone (CI) build and we install the
        latest published Nuget package and Python wheel.
#>

# Install prerequisites.
Write-Host "Installing Python prerequisites"
pip install `
    notebook jupyter_client | Write-Host

# Install IQ# dotnet tool and its jupyter kernel
$iqsharpNugetPackageRegex = 'Microsoft.Quantum.IQSharp.(\d.+).nupkg'
$buildIQSharpNugetPackageVersion = Get-ChildItem -Path $Env:NUGET_OUTDIR -ErrorAction SilentlyContinue`
                                    | where { $_.Name -match $iqsharpNugetPackageRegex } `
                                    | foreach { $matches[1] }

if ($buildIQSharpNugetPackageVersion) {
    # Uninstall if different version is already installed
    try {
        $currentInstalledVersion = dotnet tool list --global | Select-String -Pattern "microsoft.quantum.iqsharp\s+(.*)\s+" | foreach { $matches[1] }
        if ($currentInstalledVersion -and ($currentInstalledVersion -ne $buildIQSharpNugetPackageVersion)) {
            Write-Host "IQ# dotnet tool is already installed with a different version."
            Write-Host "Uninstalling version $currentInstalledVersion"
            dotnet tool uninstall --global Microsoft.Quantum.IQSharp | Write-Host
        }
    } catch {}

    Write-Host "Installing the IQ# dotnet tool specific version from the build drop folder."
    Write-Host "  Version: $buildIQSharpNugetPackageVersion"
    Write-Host "  Source: $Env:NUGET_OUTDIR"
    
    dotnet tool install --global Microsoft.Quantum.IQSharp --version $buildIQSharpNugetPackageVersion --add-source $Env:NUGET_OUTDIR | Write-Host
} else {
    Write-Host "Installing the latest published IQ# dotnet tool"
    dotnet tool install --global Microsoft.Quantum.IQSharp | Write-Host
}

Write-Host "Installing the IQ# Kernel from the installed tool"
dotnet iqsharp install --user | Write-Host

# Install the qsharp Python wheel
$qsharpPythonWheel = 'qsharp-(\d.+)-py3-none-any.whl'
$buildQSharpPythonWheelPath = Get-ChildItem -Path $Env:PYTHON_OUTDIR -ErrorAction SilentlyContinue `
                                    | where { $_.Name -match $qsharpPythonWheel } `
                                    | foreach { $_.FullName }

if ($buildQSharpPythonWheelPath) {
    Write-Host "Installing the qsharp Python wheel from the build drop folder."
    Write-Host "  Wheel: $buildQSharpPythonWheelPath"
    Write-Host "  Source: $Env:PYTHON_OUTDIR"
    pip install --verbose --no-index --find-links=$Env:PYTHON_OUTDIR qsharp | Write-Host
} else {
    Write-Host "Installing the latest published qsharp Python package"
    pip install qsharp | Write-Host
}
