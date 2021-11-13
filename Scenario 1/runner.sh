#!/bin/bash
#needs unconfined due to Alpine/ARM bug https://github.com/alpinelinux/docker-alpine/issues/135
echo "Starting Containers..."
for i in {5..55}
do
    docker run --security-opt seccomp=unconfined --net iotnet --ip 172.18.0.$i -w /var/lib/iotsim/s1/ -d -i "iot-sim1" ./launch_node.sh 172.18.0.$i iot$i
done

echo "Done."
#quick debug launch 
#sudo docker run --security-opt seccomp=unconfined --net iotnet --ip 172.18.0.2 -w /var/lib/iotsim/s1 -t -i "iot-sim1" /bin/sh
