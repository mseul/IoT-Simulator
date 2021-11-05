#!/bin/sh -x
nohup python ./receiver.py --localip=$1 --isrelay=1 &
nohup python ./generator.py --localip=$1 --nodename=$2 &
