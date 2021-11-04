#!/bin/sh
nohup python ./receiver.py &
nohup python ./generator.py &
