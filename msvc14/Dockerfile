FROM microsoft/windowsservercore:10.0.14393.1884

LABEL maintainer="Uilian Ries <uilianries@gmail.com>"

SHELL ["powershell.exe", "-ExecutionPolicy", "Bypass", "-Command"]

ENV chocolateyUseWindowsCompression=false \
    PYTHONIOENCODING=UTF-8

RUN Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))

RUN choco install --yes python2  --params '"/InstallDir:C:\tools\python27"'
RUN pip install --no-cache-dir conan conan-package-tools win-unicode-console

RUN choco install --yes cmake --installargs 'ADD_CMAKE_TO_PATH=""System""'

RUN choco install --yes --execution-timeout=7200 vcbuildtools -ia "/Full"

RUN mkdir "C:\.conan"
WORKDIR "C:\Users\ContainerAdministrator"
#SHELL ["cmd.exe", "/s", "/c"]
ENTRYPOINT ["cmd.exe", "C:\\Program Files (x86)\\Microsoft Visual C++ Build Tools\\vcbuildtools_msbuild.bat"]

