#!/usr/bin/python

import os
import sys
import subprocess

if __name__ == "__main__":
    username = os.getenv("DOCKER_USERNAME", "")
    password = os.getenv("DOCKER_PASSWORD", "").replace('"', '\\"')
    upload = os.getenv("DOCKER_UPLOAD", False)
    branch = os.getenv("TRAVIS_BRANCH", "")
    stable_branch = os.getenv("DOCKER_STABLE_BRANCH", "master")
    service = os.getenv("DOCKER_SERVICE", "")

    subprocess.check_call(["docker-compose", "build", service])

    if not upload:
        print("Skiping upload, the option is disabled.")
        sys.exit(0)

    if stable_branch != branch:
        print("Skiping upload, branch %s is not stable" % branch)
        sys.exit(0)

    if not password:
        print("Could not upload, password was not defined.")
        sys.exit(1)

    if not username:
        print("Could not upload, username was not defined.")
        sys.exit(1)

    subprocess.check_call(["docker", "login", "-u", username, "-p", password])
    subprocess.check_call(["docker-compose", "push"])
