#!/bin/bash
#needs unconfined due to Alpine/ARM bug https://github.com/alpinelinux/docker-alpine/issues/135
echo "Starting Containers..."
for i in {5..55}
do
    docker run --security-opt seccomp=unconfined --net iotnet --ip 172.18.0.$i -d -i "iot-sim2" /bin/bash 172.18.0.$i iot$i &
done

echo "Done."
#quick debug launch 
#sudo docker run --security-opt seccomp=unconfined --net iotnet --ip 172.18.0.2 -d -i "iot-sim2" /bin/sh

#ssh -i id_rsa_shared root@172.18.0.2
