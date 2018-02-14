FROM microsoft/nanoserver:10.0.14393.2068

LABEL maintainer="Uilian Ries <uilianries@gmail.com>"

SHELL ["powershell.exe", "-ExecutionPolicy", "Bypass", "-Command"]

ENV chocolateyUseWindowsCompression=false \
    PYTHONIOENCODING=UTF-8

RUN Set-ExecutionPolicy Bypass -Scope Process -Force; iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex

RUN choco install --yes python2  --params '"/InstallDir:C:\tools\python27"'
RUN pip install --no-cache-dir conan conan-package-tools win-unicode-console

RUN choco install --yes cmake --installargs 'ADD_CMAKE_TO_PATH=""System""'

RUN choco install --yes visualstudio2017buildtools --pacakge-parameters "--includeRecommend --includeOptional"
RUN choco install --yes visualstudio2017-workload-vctools "--includeRecommend --includeOptional"

RUN mkdir "C:\.conan"
WORKDIR "C:\Users\ContainerAdministrator"
CMD ["powershell.exe", "-nologo"]
