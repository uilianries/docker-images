# Copyright (C) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license. See LICENSE.txt in the project root for license information.
FROM microsoft/windowsservercore:10.0.14393.1884

LABEL maintainer="Uilian Ries <uilianries@gmail.com>"

SHELL ["powershell.exe", "-ExecutionPolicy", "Bypass", "-Command"]

ENV chocolateyUseWindowsCompression=false \
    PYTHONIOENCODING=UTF-8 \
    VS140COMNTOOLS="C:\\Program Files (x86)\\Microsoft Visual Studio\\2015\\BuildTools\\Common7\\Tools\\"
	
RUN Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

RUN choco install --yes python2  --params '"/InstallDir:C:\tools\python27"'
RUN pip install --no-cache-dir conan conan-package-tools win-unicode-console

RUN choco install --yes cmake --installargs 'ADD_CMAKE_TO_PATH=""System""'

RUN choco install --yes VisualCppBuildTools -packageParameters "--Features Win81SDKCppBuildSKUV1"

RUN Write-Host 'Updating PATH ...'; \
    $env:PATH = 'C:\Program Files (x86)\Microsoft Visual Studio\2017\BuildTools\Common7\Tools;' + $env:PATH; \
    [Environment]::SetEnvironmentVariable('PATH', $env:PATH, [EnvironmentVariableTarget]::Machine);

# Use shell form to start developer command prompt and any other commands specified
SHELL ["cmd.exe", "/s", "/c"]
ENTRYPOINT "VsDevCmd.bat" &&

# Default to PowerShell console running within developer command prompt environment
CMD ["cmd.exe"]

