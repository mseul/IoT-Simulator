#!/bin/bash
ssh-keygen -t rsa -b 4096 -f ./compliance_server_shared
ssh-keygen -t rsa -b 4096 -f ./peering_key