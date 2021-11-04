# IoT Simulator
 
Proof-of-Concept code for DFSC5336 research project.

Generates series of simulated data submissions to a threaded TCP server.
Client supports automatically switching connections to a peer or known other server if main connection severed.
Server can be run in terminal or relay mode to facilitate p2p relaying.
Client can induce errors and corrupt data to test local verification scenarios.

All code compatible with Python 3.7.x and newer.
