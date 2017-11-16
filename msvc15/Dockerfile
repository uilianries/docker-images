# Copyright (C) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license. See LICENSE.txt in the project root for license information.
FROM microsoft/windowsservercore:10.0.14393.1884

LABEL maintainer="Uilian Ries <uilianries@gmail.com>"

SHELL ["powershell.exe", "-ExecutionPolicy", "Bypass", "-Command"]

ENV TEST_CONTAINER=1 \
    VS_CHANNEL_URI=https://aka.ms/vs/15/release/799c44140/channel \
    VS_BUILDTOOLS_URI=https://aka.ms/vs/15/release/799c44140/vs_buildtools.exe \
    VS_BUILDTOOLS_SHA256=FA29EB83297AECADB0C4CD41E54512C953164E64EEDD9FB9D3BF9BD70C9A2D29 \
    NUGET_URI=https://dist.nuget.org/win-x86-commandline/v4.1.0/nuget.exe \
    NUGET_SHA256=4C1DE9B026E0C4AB087302FF75240885742C0FAA62BD2554F913BBE1F6CB63A0

# Download nuget.exe
RUN $ErrorActionPreference = 'Stop'; \
    $ProgressPreference = 'SilentlyContinue'; \
    $VerbosePreference = 'Continue'; \
    New-Item -Path C:\bin -Type Directory | Out-Null; \
    [System.Environment]::SetEnvironmentVariable('PATH', "\"${env:PATH};C:\bin\"", 'Machine'); \
    Invoke-WebRequest -Uri $env:NUGET_URI -OutFile C:\bin\nuget.exe; \
    if ((Get-FileHash -Path C:\bin\nuget.exe -Algorithm SHA256).Hash -ne $env:NUGET_SHA256) { throw 'Download hash does not match' }

# Download log collection utility
RUN $ErrorActionPreference = 'Stop'; \
    $ProgressPreference = 'SilentlyContinue'; \
    $VerbosePreference = 'Continue'; \
    Invoke-WebRequest -Uri https://aka.ms/vscollect.exe -OutFile C:\collect.exe

# Download vs_buildtools.exe
RUN $ErrorActionPreference = 'Stop'; \
    $ProgressPreference = 'SilentlyContinue'; \
    $VerbosePreference = 'Continue'; \
    Invoke-WebRequest -Uri $env:VS_BUILDTOOLS_URI -OutFile C:\vs_buildtools.exe; \
    if ((Get-FileHash -Path C:\vs_buildtools.exe -Algorithm SHA256).Hash -ne $env:VS_BUILDTOOLS_SHA256) { throw 'Download hash does not match' }

# Install Visual Studio Build Tools
RUN $ErrorActionPreference = 'Stop'; \
    $VerbosePreference = 'Continue'; \
    $p = Start-Process -Wait -PassThru -FilePath C:\vs_buildtools.exe -ArgumentList '--quiet --nocache --wait --installPath C:\BuildTools'; \
    if ($ret = $p.ExitCode) { c:\collect.exe; throw ('Install failed with exit code 0x{0:x}' -f $ret) }

ENV PYTHON_VERSION 2.7.14
ENV PYTHON_RELEASE 2.7.14

RUN $url = ('https://www.python.org/ftp/python/{0}/python-{1}.amd64.msi' -f $env:PYTHON_RELEASE, $env:PYTHON_VERSION); \
	  Write-Host ('Downloading {0} ...' -f $url); \
	  Invoke-WebRequest -Uri $url -OutFile 'python.msi'; \
	  \
	  Write-Host 'Installing ...'; \
    # https://www.python.org/download/releases/2.4/msi/
    Start-Process msiexec -Wait \
      -ArgumentList @( \
        '/i', \
        'python.msi', \
        '/quiet', \
        '/qn', \
        'TARGETDIR=C:\Python', \
        'ALLUSERS=1', \
        'ADDLOCAL=DefaultFeature,Extensions,TclTk,Tools,PrependPath' \
        ); \
	  \
    # the installer updated PATH, so we should refresh our local value
    $env:PATH = [Environment]::GetEnvironmentVariable('PATH', [EnvironmentVariableTarget]::Machine); \
    \
    Write-Host 'Verifying install ...'; \
    Write-Host '  python --version'; python --version; \
    \
    Write-Host 'Removing ...'; \
    Remove-Item python.msi -Force; \
    \
    Write-Host 'Complete.';

# if this is called "PIP_VERSION", pip explodes with "ValueError: invalid truth value '<VERSION>'"
ENV PYTHON_PIP_VERSION 9.0.1

RUN Write-Host ('Installing pip=={0} ...' -f $env:PYTHON_PIP_VERSION); \
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; \
    Invoke-WebRequest -Uri 'https://bootstrap.pypa.io/get-pip.py' -OutFile 'get-pip.py'; \
    python get-pip.py \
        --disable-pip-version-check \
        --no-cache-dir \
        ('pip=={0}' -f $env:PYTHON_PIP_VERSION) \
    ; \
    Remove-Item get-pip.py -Force; \
    \
    Write-Host 'Verifying pip install ...'; \
    pip --version; \
    \
    Write-Host 'Complete.';

# install "conan", since the vast majority of users of this image will want it
RUN pip install --no-cache-dir conan conan-package-tools

# Use shell form to start developer command prompt and any other commands specified
SHELL ["cmd.exe", "/s", "/c"]
ENTRYPOINT C:\BuildTools\Common7\Tools\VsDevCmd.bat &&

# Default to PowerShell console running within developer command prompt environment
CMD ["powershell.exe", "-nologo"]
