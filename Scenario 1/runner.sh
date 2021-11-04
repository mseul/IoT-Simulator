#!/bin/bash
#needs unconfined due to Alpine/ARM bug https://github.com/alpinelinux/docker-alpine/issues/135
for i in {5..7}
do
    docker run --rm --security-opt seccomp=unconfined --net iotnet --ip 172.18.0.$i -w /var/lib/iotsim/s1 -d -i "iot-sim1" python ./generator.py
done

#sudo docker run --rm --security-opt seccomp=unconfined --net iotnet --ip 172.18.0.2 -w /var/lib/iotsim/s1 -t -i "iot-sim1" /bin/sh
