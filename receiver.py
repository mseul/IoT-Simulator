import socketserver
import global_settings
import sender
import validator

class myCustomServer(socketserver.ThreadingTCPServer):
    def __init__(self, hostobject, handler):
        #self.senderObj = 
        super().__init__(hostobject, handler)

class iotHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.data = str(self.request.recv(global_settings.comms_chunk_size).strip(),global_settings.comms_encoding)

        if not validator.validateInput(self.data):
            self.request.sendall(bytes(global_settings.status_code_input_invalid, global_settings.comms_encoding))
            return

        print("{0} wrote: {1}".format(self.client_address[0], self.data))
        self.request.sendall(bytes(global_settings.status_code_ok, global_settings.comms_encoding))

        if global_settings.receiver_in_relay_mode:
            print("Relaying Data...")
            try:
                sender_obj = sender.iotDataSender()
                sender_obj.sendData(self.data)
            except:
                print("Failed to send data to relay. Skipping.")

        

if __name__ == "__main__":
    with myCustomServer((global_settings.server_bind, global_settings.comms_port), iotHandler) as server:
        print ("Starting server on {0}:{1}".format(global_settings.server_bind, global_settings.comms_port))
        server.serve_forever()
