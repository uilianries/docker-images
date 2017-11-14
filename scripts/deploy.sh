#!/bin/bash

set -e

if [ "$TRAVIS_BRANCH" == "master" ]; then
    docker login -p ${DOCKER_PASSWORD} -u ${DOCKER_USERNAME}
    docker-compose push
fi

exit 0
