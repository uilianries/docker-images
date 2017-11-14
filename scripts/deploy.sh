#!/bin/bash

docker login -p ${DOCKER_PASSWORD} -u ${DOCKER_USERNAME}
docker-compose push
