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

$nugetVersion = $Env:NUGET_VERSION
$pythonVersion = $Env:PYTHON_VERSION

# Install prerequisites.
Write-Host "Installing Python prerequisites"
pip install --user `
    notebook jupyter_client | Write-Host

# Install IQ# dotnet tool (from the build drop if exists, or from Nuget.org)
$iqsharpNugetPackage = "Microsoft.Quantum.IQSharp.$nugetVersion.nupkg"
$iqsharpNugetPackagePath = !($Env:NUGET_OUTDIR) ? $iqsharpNugetPackage : (Join-Path $Env:NUGET_OUTDIR $iqsharpNugetPackage)

# PICK_QDK_VERSION="auto" is used by the E2E Live test pipeline by default
if ($Env:PICK_QDK_VERSION -eq "auto") {    
    Write-Host "Installing the latest published IQ# dotnet tool"
    dotnet tool install Microsoft.Quantum.IQSharp --tool-path $Env:TOOLS_DIR | Write-Host
}
elseif (Test-Path $iqsharpNugetPackagePath -PathType Leaf) {
    # Uninstall if different version is already installed
    try {
        $currentInstalledVersion = dotnet tool list --tool-path $Env:TOOLS_DIR | Select-String -Pattern "microsoft.quantum.iqsharp\s+(.*)\s+" | foreach { $matches[1] }
        if ($currentInstalledVersion -and ($currentInstalledVersion -ne $nugetVersion)) {
            Write-Host "IQ# dotnet tool is already installed with a different version."
            Write-Host "Uninstalling version $currentInstalledVersion"
            dotnet tool uninstall Microsoft.Quantum.IQSharp --tool-path $Env:TOOLS_DIR | Write-Host
        }
    } catch {}

    # Make sure the NUGET_OUTDIR is listed as a nuget source, otherwise
    # IQ# will fail to load when packages are loaded.
    $SourceName = "build"
    Write-Host "Adding nuget source $SourceName=$Env:NUGET_OUTDIR"
    dotnet nuget add source $Env:NUGET_OUTDIR --name $SourceName

    Write-Host "Installing the IQ# dotnet tool specific version from the build drop folder."
    Write-Host "  Version: $nugetVersion"
    Write-Host "  Source: $Env:NUGET_OUTDIR"
    
    dotnet tool install Microsoft.Quantum.IQSharp --version 0.28.302812 --tool-path $Env:TOOLS_DIR --add-source $Env:NUGET_OUTDIR | Write-Host
} else {    
    Write-Host "Installing the $nugetVersion published IQ# dotnet tool"
    dotnet tool install Microsoft.Quantum.IQSharp --version 0.28.302812 --tool-path $Env:TOOLS_DIR | Write-Host
    if ($LastExitCode -ne 0) {
        Write-Host "Installing the latest published IQ# dotnet tool"
        dotnet tool install Microsoft.Quantum.IQSharp --tool-path $Env:TOOLS_DIR | Write-Host
    }
}

Write-Host "Installing the IQ# Kernel from the installed dotnet tool"
try {
    # dotnet-iqsharp writes some output to stderr, which causes Powershell to throw
    # unless $ErrorActionPreference is set to 'Continue'.
    $ErrorActionPreference = 'Continue'
    $path = (Get-Item "$Env:TOOLS_DIR\dotnet-iqsharp*").FullName
    # Redirect stderr output to stdout to prevent an exception being incorrectly thrown.
    & $path install --user --path-to-tool $path 2>&1 | Write-Host
    Write-Host "iq# kernel installed ($LastExitCode)"
} catch {
    Write-Host ("iq# installation threw error: " + $_)
    Write-Host ("iq# might not be correctly installed.")
} finally {
    $ErrorActionPreference = 'Stop'
}

# Install the qsharp Python wheel
$qsharpPythonWheel = "qsharp-$pythonVersion-py3-none-any.whl"
$qsharpPythonWheelPath = !($Env:PYTHON_OUTDIR) ? $qsharpPythonWheel : (Join-Path $Env:PYTHON_OUTDIR $qsharpPythonWheel)

# PICK_QDK_VERSION="auto" is used by the E2E Live test pipeline by default
if ($Env:PICK_QDK_VERSION -eq "auto") {    
    Write-Host "Installing the latest published qsharp Python package"
    pip install --user --verbose qsharp | Write-Host
} elseif (Test-Path $qsharpPythonWheelPath -PathType Leaf) {
    Write-Host "Installing the qsharp Python wheel from the build drop folder."
    Write-Host "  Wheel: $qsharpPythonWheelPath"
    Write-Host "  Source: $Env:PYTHON_OUTDIR"
    pip install --user --verbose --no-index --find-links=$Env:PYTHON_OUTDIR "qsharp==$pythonVersion" | Write-Host
} else {
    Write-Host "Installing the $pythonVersion published qsharp Python package"
    pip install --user --verbose "qsharp==$pythonVersion" | Write-Host
    if ($LastExitCode -ne 0) {
        Write-Host "Installing the latest published qsharp Python package"
        pip install --user --verbose qsharp | Write-Host
    }
}

exit 0
