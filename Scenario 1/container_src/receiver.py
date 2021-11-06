import socketserver
import global_settings
import sender
import validator
import time
import random
import argparse
import threading
import itertools

#By JULIEN DANJOU
#https://julien.danjou.info/atomic-lock-free-counters-in-python/
class FastWriteCounter(object):
    def __init__(self):
        self._number_of_read = 0
        self._counter = itertools.count()
        self._read_lock = threading.Lock()

    def increment(self):
        next(self._counter)

    def value(self):
        with self._read_lock:
            value = next(self._counter) - self._number_of_read
            self._number_of_read += 1
        return value

launch_time = None
receiver_enforcement_active = False
myArgs = None
statsPrintTimer = None
totalStatsLastInterval = 0
counterRQokay = FastWriteCounter()
counterRQerror = FastWriteCounter()

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
        
        if not receiver_enforcement_active:
            global launch_time
            if (global_settings.receiver_enforce_authorized_senders_time_sec > 0) and ((time.time() - launch_time) >= global_settings.receiver_enforce_authorized_senders_time_sec):
                 receiver_enforcement_active = True

        while True:

            global counterRQerror
            global counterRQokay

            if receiver_enforcement_active:
                if not self.client_address[0] in global_settings.authorized_senders:
                    print("Rejecing {0}, not on list of authorized senders.".format(self.client_address[0]))
                    #counterRQerror.increment() #Not counting this as an error for now
                    self.request.sendall(bytes(global_settings.status_code_server_error, global_settings.comms_encoding))
                    return #leave function to kill off connection after rejection message

            self.data = str(self.request.recv(global_settings.comms_chunk_size).strip(),global_settings.comms_encoding)
            #print("{0} wrote: {1}".format(self.client_address[0], self.data))

            if (self.data == global_settings.status_code_rq_done):
                return #Leave function, we're done here

            if not validator.validateInput(self.data):
                counterRQerror.increment()
                self.request.sendall(bytes(global_settings.status_code_input_invalid, global_settings.comms_encoding))
            else:
                counterRQokay.increment()
                self.request.sendall(bytes(global_settings.status_code_ok, global_settings.comms_encoding))

        if myArgs.isrelay:
            print("Relaying Data...")
            try:
                global localip
                sender_obj = sender.iotDataSender(myIP = myArgs.localip)
                sender_obj.sendData(self.data)
            except:
                print("Failed to send data to relay. Skipping.")

def printStats():
    global counterRQokay
    global counterRQerror
    global launch_time
    global totalStatsLastInterval

    time_passed = (time.time() - launch_time)
    rqOkay = counterRQokay.value()
    rqError = counterRQerror.value()
    requests_total = rqOkay + rqError

    requestPerSec = (requests_total - totalStatsLastInterval) / global_settings.statsPrintInterval
    totalStatsLastInterval = requests_total

    print("{time},{total},{per_sec},{okay},{error}".format(time=time_passed,total=requests_total,per_sec=requestPerSec,okay=rqOkay,error=rqError))

    statsPrintTimer = threading.Timer(global_settings.statsPrintInterval, printStats)
    statsPrintTimer.start()



if __name__ == "__main__":
    myArgs = arg_parse()
    random.shuffle(global_settings.peer_nodes)

    statsPrintTimer = threading.Timer(global_settings.statsPrintInterval, printStats)
    statsPrintTimer.start()

    if (myArgs.isrelay == 1):
        print("Operating in RELAY mode.")
    else:
        print("Operating in TERMINAL mode.")

    with myCustomServer((global_settings.server_bind, global_settings.comms_port), iotHandler) as server:
        print ("Starting server on {0}:{1}".format(global_settings.server_bind, global_settings.comms_port))
        launch_time = time.time()
        print("Seconds since Launch,Total Requests,Requests Per Sec,Requests Okay, Requests Error")
        server.serve_forever()
