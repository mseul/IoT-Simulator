#!/bin/sh
echo "Starting Receiver..."
nohup python ./receiver.py --localip=$1 --isrelay=1 &
echo "Starting Generator..."
nohup python ./generator.py --localip=$1 --nodename=$2 &
echo "Node launched."

#python ./generator.py --localip=172.18.0.2 --nodename=iot2

echo "Process running. Press CTRL+C to exit."
while true
do
	sleep 10
done