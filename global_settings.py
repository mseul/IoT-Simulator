curveStep = 0
curveMod = 15
rotAmplifier = 1000
curveFloor = 800
curveCeiling = curveMod * rotAmplifier
sleepMin = 10
sleepMax = 200
sleepDivide = 10000
comms_port = 1337
comms_chunk_size = 1024
comms_encoding = "utf-8"
server_bind = "0.0.0.0"
status_code_ok = "200"
status_code_server_error = "500"
status_code_input_invalid = "400"
data_format = "{id}##{value}"

receiver_in_relay_mode = False
targetDir = "/var/log/iot-capture/"
terminal_receivers = ["121.0.0.1"]
switch_to_peers_immediately = False
peer_nodes = ["127.0.0.1"]
authorized_senders = []
node_identifier = "iot0-1fd78078"
