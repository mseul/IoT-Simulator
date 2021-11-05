import socketserver
import global_settings
import sender
import validator
import time
import random

launch_time = None
receiver_enforcement_active = False
myArgs = None

import argparse

def arg_parse():
    theParser = argparse.ArgumentParser(description="IoT Simulator")
    theParser.add_argument("--localip", dest="localip", action="store", required=True)
    theParser.add_argument("--isrelay", dest="isrelay", type=int, action="store", required=True)
    return theParser.parse_args()

class myCustomServer(socketserver.ThreadingTCPServer):
    def __init__(self, hostobject, handler):
        super().__init__(hostobject, handler)

class iotHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global receiver_enforcement_active
        global launch_time
        global localip
        
        if not receiver_enforcement_active:
            if (global_settings.receiver_enforce_authorized_senders_time_sec > 0) and ((time.time() - launch_time) >= global_settings.receiver_enforce_authorized_senders_time_sec):
                 receiver_enforcement_active = True

        if receiver_enforcement_active:
            if not self.client_address[0] in global_settings.authorized_senders:
                print("Rejecing {0}, not on list of authorized senders.".format(self.client_address[0]))
                self.request.sendall(bytes(global_settings.status_code_server_error, global_settings.comms_encoding))

        self.data = str(self.request.recv(global_settings.comms_chunk_size).strip(),global_settings.comms_encoding)

        if not validator.validateInput(self.data):
            self.request.sendall(bytes(global_settings.status_code_input_invalid, global_settings.comms_encoding))
            return

        print("{0} wrote: {1}".format(self.client_address[0], self.data))
        self.request.sendall(bytes(global_settings.status_code_ok, global_settings.comms_encoding))

        if myArgs.isrelay:
            print("Relaying Data...")
            try:
                sender_obj = sender.iotDataSender(myIP = myArgs.localip)
                sender_obj.sendData(self.data)
            except:
                print("Failed to send data to relay. Skipping.")
 

if __name__ == "__main__":
    myArgs = arg_parse()
    random.shuffle(global_settings.peer_nodes)

    if (myArgs.isrelay == 1):
        print("Operating in RELAY mode.")
    else:
        print("Operating in TERMINAL mode.")

    with myCustomServer((global_settings.server_bind, global_settings.comms_port), iotHandler) as server:
        print ("Starting server on {0}:{1}".format(global_settings.server_bind, global_settings.comms_port))
        launch_time = time.time()
        server.serve_forever()
