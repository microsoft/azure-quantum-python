
Import-Module (Join-Path $PSScriptRoot "conda-utils.psm1");

function PackagesList{
    param(
        [string] $PackageName
    )
    if ('' -eq $PackageName) {
        # If no package dir is specified, find all packages that contain an environment.yml file
        $parentPath = Split-Path -parent $PSScriptRoot
        $PackageNames = Get-ChildItem -Path $parentPath -Recurse -Filter "environment.yml" | Select-Object -ExpandProperty Directory | Split-Path -Leaf
        Write-Host "##[info]No PackageDir. Setting to default '$PackageNames'"
    } else {
        $PackageNames = @($PackageName)
    }
    return $PackageNames
}

function Install-Package() {
    param(
        [string] $EnvName,
        [string] $PackageName,
        [bool] $FromSource,
        [string] $BuildArtifactPath
    )
    # Activate env
    Use-CondaEnv $EnvName
    # Install package
    if ($True -eq $FromSource) {
        $ParentPath = Split-Path -parent $PSScriptRoot
        $AbsPackageName = Join-Path $ParentPath $PackageName
        Write-Host "##[info]Install package $AbsPackageName in development mode for env $EnvName"
        pip install -e $AbsPackageName
    } elseif ("" -ne $BuildArtifactPath) {
        Write-Host "##[info]Installing $PackageName from $BuildArtifactPath"
        Push-Location $BuildArtifactPath
            pip install $PackageName --pre --find-links $BuildArtifactPath
            if ($LASTEXITCODE -ne 0) { throw "Error installing qsharp-core wheel" }
        Pop-Location
    } else {
        Write-Host "##[info]Install package $PackageName for env $EnvName"
        pip install $PackageName
    }
}

function GetEnvName {
    param (
        [string] $PackageName,
        [string] $CondaEnvironmentSuffix
    )
    # The environment name is based on $PackageName, but
    #   1. if the name includes the version via name==version, remove the version, 
    #   2. add conda env suffix
    #   3. remove "-" since its invalid
    #   4. remove ".aio" and use the same environment as the non-async version
    return ($PackageName.Split("=")[0] + $CondaEnvironmentSuffix).replace("-", "").replace(".aio", "")
}

function Install-PackageInEnv {
    param (
        [string] $PackageName,
        [string] $CondaEnvironmentSuffix,
        [bool] $FromSource,
        [string] $BuildArtifactPath
    )
    $PackageNames = PackagesList -PackageName $PackageName
    foreach ($PackageName in $PackageNames) {
        $EnvName = GetEnvName -PackageName $PackageName -CondaEnvironmentSuffix $CondaEnvironmentSuffix
        Install-Package -EnvName $EnvName -PackageName $PackageName -FromSource $FromSource -BuildArtifactPath $BuildArtifactPath
    }
}

function New-CondaEnvironment {
    param(
        [string] $PackageName,
        [string] $CondaEnvironmentSuffix
    )
    <#
        .SYNOPSIS
            Create Conda environment(s) for given package directories
            Optionally, use CondaEnvironmentSuffix to specify a special environment file with name environment<CondaEnvironmentSuffix>.yml.
            If PackageName is not specified, get all packages in the root directory.
    #>

    $PackageNames = PackagesList -PackageName $PackageName
    foreach ($PackageName in $PackageNames) {
        $Name = GetEnvName $PackageName
        NewCondaEnvForPackage -PackageName $Name -CondaEnvironmentSuffix $CondaEnvironmentSuffix
    }
}

function NewCondaEnvForPackage {
    param(
        [string] $PackageName,
        [string] $CondaEnvironmentSuffix
    )
    <#
        .SYNOPSIS
            Create Conda environment(s) for given package directories
            Optionally, use CondaEnvironmentSuffix to specify a special environment file with name environment<CondaEnvironmentSuffix>.yml.
    #>

    $parentPath = Split-Path -parent $PSScriptRoot
    $EnvPath = Join-Path $parentPath $PackageName "environment$CondaEnvironmentSuffix.yml"
    $EnvName = GetEnvName -PackageName $PackageName -CondaEnvironmentSuffix $CondaEnvironmentSuffix

    # Check if environment already exists
    $EnvExists = conda env list | Select-String -Pattern "$EnvName " | Measure-Object | Select-Object -Exp Count

    # If it exists, skip creation
    if ($EnvExists -eq "1") {
        Write-Host "##[info]Skipping creating $EnvName; env already exists."

    } else {
        # If it does not exist, create conda environment
        Write-Host "##[info]Build '$EnvPath' for Conda environment $EnvName"
        conda env create --quiet --file $EnvPath
    }    
}

function New-Wheel() {
    param(
        [string] $EnvName,
        [string] $Path,
        [string] $OutDir
    );

    Push-Location $Path
        # Set environment vars to be able to run conda activate
        Write-Host "##[info]Pack wheel for env '$EnvName'"
        # Activate env
        Use-CondaEnv $EnvName
        # Create package distribution
        python setup.py bdist_wheel sdist --formats=gztar

        if  ($LastExitCode -ne 0) {
        Write-Host "##vso[task.logissue type=error;]Failed to build $Path."
        $script:all_ok = $False
        } else {
            if ($OutDir -ne "") { 
                Write-Host "##[info]Copying wheel to '$OutDir'"
                Copy-Item "dist/*.whl" $OutDir/
                Copy-Item "dist/*.tar.gz" $OutDir/
            }
        }
    Pop-Location
}


function Invoke-Tests() {
    param(
        [string] $PackageName,
        [string] $EnvName
    )
    $ParentPath = Split-Path -parent $PSScriptRoot
    $AbsPackageDir = Join-Path $ParentPath $PackageName
    Write-Host "##[info]Test package $AbsPackageDir and run tests for env $EnvName"
    # Activate env
    Use-CondaEnv $EnvName
    # Install testing deps
    python -m pip install --upgrade pip | Write-Host
    pip install pytest pytest-azurepipelines pytest-cov | Write-Host
    # Run tests
    $PkgName = $PackageName.replace("-", ".")
    pytest --cov-report term --cov=$PkgName --junitxml test-output-$PackageName.xml $AbsPackageDir | Write-Host
    return ($LASTEXITCODE -eq 0)
}
