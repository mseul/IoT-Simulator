# IoT Simulator
 
Proof-of-Concept code for DFSC5336 research project.

SCENARIO 1
Generates series of simulated data submissions to a threaded TCP server.
Client supports automatically switching connections to a peer or known other server if main connection severed.
Server can be run in terminal or relay mode to facilitate p2p relaying.
Client can induce errors and corrupt data to test local verification scenarios.

The scenario uses Apline Linux with Python 3.9 as a mix-in.
No additional pip modules are used.
This is done to simulate an evironment closer to embedded or IoT systems. 

Use builder.sh to generate docker container.
Start receiver.py in Terminal mode on destination system.
Use runner.sh to launch 50 nodes.
Stats will appear on Terminal and updated approx. every 2 seconds.


SCENARIO 2

Purely proof of concept script to show that with very little additional scripting, a host can be deputized to replay complex compliance checking commands against a peer.
The scenario uses Alpine with Busybox on ARM7 to simulate an environment commonly found on embedded or IoT systems.
Apart from OpenSSH for connectivity, no further elements are installed.

Audit calls are based on the CIS Benchmark v2.0.0 for generic Linux distributions.

Review testcall.txt for an example of how to use the audit_replay.sh.

Please note that this scenario has a few assumptions:

* Peers have a pre-authorized SSH key to SSH into each other
* Peers have the audit_replay.sh locally and with execute rights

These two assumptions were made purely for convenience and getting the project done within the timeframe.
In a real-world scenario, one could manage key distribution via dedicated users or time-sliced access.

Also, one could use an initial command to deploy the Bash script, instead of assuming its presence.
Given that all tools, apart from openSSH are included in even the most basic distribtion, it should be transferable to may different platforms.



All code compatible with Python 3.7.x and newer.
Runs on ARM7 and Regular 86x64 systems.
