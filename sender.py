import socket
import sys
import random
import global_settings

class iotDataSender:
    def __init__(self):
        self.currentHost = global_settings.terminal_receivers[0]
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.onPeerFallback = False

    def sendData(self, data):
        transferStatus = None
        while True:
            try:
                # Connect to server and send data
                self.socket.sendall(bytes(data+ "\n", global_settings.comms_encoding))
                print("Sent:     {}".format(data))

                # Receive data from the server and shut down
                transferStatus = str(self.socket.recv(global_settings.comms_chunk_size), global_settings.comms_encoding)
                print("Received: {}".format(transferStatus))
                self.socket.close()
                return
            except:
                if not self.establishConnection():
                    raise

    def establishConnection(self):
        targetServer = self.currentHost
        print("Establishing connection...")
        
        while True:
            try:
                print("Connecting to {0}:{1}".format(targetServer, str(global_settings.comms_port)))
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((targetServer, global_settings.comms_port))
                self.currentHost = targetServer
                return True
            except:
                print("Connecting failed. Switching server.")
                targetServer = self.handleServerSwitch(targetServer)
                if targetServer == None:
                    print("Out of viable servers. Connection failed.")
                    return False

    def handleServerSwitch(self, failedServer):
        if (global_settings.switch_to_peers_immediately) or (self.onPeerFallback):
            listToWork = global_settings.peer_nodes
            self.onPeerFallback = True
        else:
            listToWork = global_settings.terminal_receivers

        while True:
            for aServer in listToWork:
                if not (aServer == failedServer):
                    return aServer

            if self.onPeerFallback:
                return None
            
            print("Switching to peer nodes for connection.")
            listToWork = global_settings.peer_nodes
            self.onPeerFallback = True







# Create a socket (SOCK_STREAM means a TCP socket)


