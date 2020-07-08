#!/usr/bin/env bash
docker build --build-arg DOCKER_GID=`id -u` --build-arg DOCKER_UID=`id -g` -t mbari/deepsea-imagecropper .
