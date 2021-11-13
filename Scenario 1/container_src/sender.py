import socket
import sys
import random
import global_settings
import socket
import sys
import errno

class iotDataSender:
    def __init__(self, myIP = global_settings.default_not_defined_str, usebrokenterminal = global_settings.client_uses_broken_terminal_threshold):

        self.currentHost = global_settings.terminal_receivers[0]

        if usebrokenterminal > 0:
            if random.randrange(1,10) > global_settings.client_uses_broken_terminal_threshold:
                print("This client starts off with a broken connection.")
                self.currentHost = global_settings.terminal_receivers_broken[0]

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.onPeerFallback = False
        self.peerListPosition = 0
        self.mainIP = myIP

    def sendData(self, data):
        transferStatus = None
        while True:
            try:
                # Connect to server and send data
                self.socket.sendall(bytes(data+ "\n", global_settings.comms_encoding))
                #print("Sent:     {}".format(data))

                # Receive data from the server and shut down
                transferStatus = str(self.socket.recv(global_settings.comms_chunk_size), global_settings.comms_encoding)
                #print("Received: {}".format(transferStatus))

                if transferStatus == global_settings.status_code_ok:
                    #print("Request OK")
                    pass
                elif transferStatus == global_settings.status_code_server_error:
                    print("Server reported internal error. Forcing server switch.")
                    self.currentHost = self.handleServerSwitch(self.currentHost)
                    raise ConnectionAbortedError
                elif transferStatus == global_settings.status_code_input_invalid:
                    #print("Server rejected data submitted as invalid. Discarding data.")
                    pass
                else:
                    print("Received an unspecified status code '{code}' from server. Forcing server switch.".format(code=transferStatus))
                    self.currentHost = self.handleServerSwitch(self.currentHost)
                    raise ConnectionAbortedError

                #self.socket.close()
                return
            except KeyboardInterrupt:
                raise
            except:
                if not self.establishConnection():
                    raise                
            # except ConnectionResetError:
            #         if not self.establishConnection():
            #             raise
            # except ConnectionRefusedError:
            #         if not self.establishConnection():
            #             raise
            # except BrokenPipeError:
            #         if not self.establishConnection():
            #             raise
            # except ConnectionAbortedError:
            #         if not self.establishConnection():
            #             raise
            # except OSError as theError:
            #         if not self.establishConnection():
            #             raise
            # else:
            #     raise

    def establishConnection(self):
        targetServer = self.currentHost
        #print("Establishing connection...")

        if targetServer == None:
            print("No valid target server. Connection failed.")
            return False
        
        while True:
            try:
                if (targetServer == self.mainIP):
                    raise Exception("Loopback connection detected. Rejecting this connection attempt.")

                print("Connecting to {0}:{1}".format(targetServer, str(global_settings.comms_port)))
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((targetServer, global_settings.comms_port))
                self.currentHost = targetServer
                return True
            except KeyboardInterrupt:
                raise
            except:
                print("Connecting to {0}:{1} failed. Switching server.".format(targetServer, str(global_settings.comms_port)))
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

        listLen = len(listToWork)

        while True:
            aServer = listToWork[self.peerListPosition]
            self.peerListPosition += 1

            if (not (aServer == failedServer)) and (not (aServer == self.mainIP)):
                return aServer
            
            if self.peerListPosition < listLen:
                continue

            if self.onPeerFallback:
                return None
            
            print("Switching to peer nodes for connection.")
            listToWork = global_settings.peer_nodes
            self.onPeerFallback = True
            self.peerListPosition = 0
