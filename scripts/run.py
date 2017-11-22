#!/usr/bin/python

import os
import sys
import subprocess
import platform
import re

class Runner(object):

    def __init__(self):
        self.username = os.getenv("DOCKER_USERNAME", "")
        self.password = os.getenv("DOCKER_PASSWORD", "").replace('"', '\\"')
        self.upload = os.getenv("DOCKER_UPLOAD", False)
        travis_branch = os.getenv("TRAVIS_BRANCH", "")
        appveyor_branch = os.getenv("APPVEYOR_REPO_BRANCH","")
        self.stable_branch = os.getenv("DOCKER_STABLE_BRANCH", "master")
        self.service = os.getenv("DOCKER_SERVICE", "")
        self.branch = travis_branch if travis_branch != "" else appveyor_branch
        self.compiler = "Visual Studio" if platform.system() == "Windows" else "gcc"
        version_match = re.match(r"\D+(\d+).*", self.service)
        self.compiler_version = version_match.group(1) if platform.system() == "Windows" else '.'.join(version_match.group(1))
        self.cross_building = "arm" in self.service
        self.image = "%s/%s" % (self.username, self.service)

    def build(self):
        subprocess.check_call(["docker-compose", "build", self.service])

    def test(self):
        try:
            update_command = ["docker", "exec", self.service, "sudo", "pip", "install", "-U", "conan"]
            if platform.system() == "Windows":
                update_command.remove("sudo")

            subprocess.check_call(["docker", "run", "-t", "-d", "--name", self.service, self.image])
            subprocess.check_call(update_command)
            subprocess.check_call(["docker", "exec", self.service, "conan", "user"])

            if self.cross_building:
                subprocess.check_call(["docker", "exec", "-e", "CC=arm-linux-gnueabihf-gcc", "-e", "CXX=arm-linux-gnueabihf-g++",
                                        self.service, "conan", "install", "zlib/1.2.11@conan/stable",
                                        "-s", "arch=armv7", "-s", "compiler=gcc", "-s", "compiler.version=%s" % self.compiler_version,
                                        "--build"])
            else:
                subprocess.check_call(["docker", "exec", self.service, "conan", "install", "zlib/1.2.11@conan/stable",
                                        "-s", "arch=x86", "-s", "compiler=%s" % self.compiler, "-s", "compiler.version=%s" % self.compiler_version,
                                        "--build"])
                subprocess.check_call(["docker", "exec", self.service, "conan", "install", "zlib/1.2.11@conan/stable",
                                    "-s", "arch=x86_64", "-s", "compiler=%s" % self.compiler, "-s", "compiler.version=%s" % self.compiler_version,
                                    "--build"])
                subprocess.check_call(["docker", "exec", self.service, "conan", "remote", "add", "conan-community",
                                   "https://api.bintray.com/conan/conan-community/conan", "--insert"])
                subprocess.check_call(["docker", "exec", self.service, "conan", "install", "gtest/1.8.0@conan/stable",
                                        "-s", "arch=x86_64", "-s", "compiler=%s" % self.compiler, "-s", "compiler.version=%s" % self.compiler_version,
                                        "--build"])
                subprocess.check_call(["docker", "exec", self.service, "conan", "install", "gtest/1.8.0@conan/stable",
                                        "-s", "arch=x86", "-s", "compiler=%s" % self.compiler, "-s", "compiler.version=%s" % self.compiler_version,
                                        "--build"])
        finally:
            subprocess.call(["docker", "stop", self.service])
            subprocess.call(["docker", "rm", self.service])

    def deploy(self):
        if not self.upload:
            print("Skiping upload, the option is disabled.")
            sys.exit(0)

        if self.stable_branch != self.branch:
            print("Skiping upload, branch %s is not stable" % self.branch)
            sys.exit(0)

        if not self.username:
            print("Could not upload, username was not defined.")
            sys.exit(1)

        if not self.password:
            print("Could not upload, password was not defined.")
            sys.exit(1)

        subprocess.check_call(["docker", "login", "-u", self.username, "-p", self.password])
        subprocess.check_call(["docker-compose", "push", self.service])

    def run(self):
        self.build()
        self.test()
        self.deploy()

if __name__ == "__main__":
    runner = Runner()
    runner.run()
