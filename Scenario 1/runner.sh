#!/bin/bash
#needs unconfined due to Alpine/ARM bug https://github.com/alpinelinux/docker-alpine/issues/135
sudo docker run --rm --security-opt seccomp=unconfined --net iotnet --ip 172.18.0.23 --publish 1337:1337 -w /var/lib/iotsim/s1 -t -i "python:3-alpine" /bin/sh