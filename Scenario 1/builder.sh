#!/bin.bash

#The below commands enable forwarding to allow the bridge to interact with the local network
#Uncomment if this functionality is needed, otherwise leave as is
#See https://docs.docker.com/network/bridge/#enable-forwarding-from-docker-containers-to-the-outside-world
#sysctl net.ipv4.conf.all.forwarding=1
#iptables -P FORWARD ACCEPT

docker network create --subnet=172.18.0.0/16 iotnet
docker build -t "python:3-alpine" .