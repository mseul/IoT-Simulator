import socketserver
import global_settings
import sender
import validator
import time
import random
import argparse
import threading
import fastwritecounter

class LockedIotSender:
    def __init__(self, myIP = global_settings.default_not_defined_str):
        self.IoTSender = sender.iotDataSender(myIP = myIP)
        self.lock = threading.Lock()

class lockedIotSenderPool:
    def __init__(self, myIP = global_settings.default_not_defined_str):
        self.pool = dict()
        self.myIP = myIP
        self.lock = threading.Lock()
    
    def getIoTSender(self, identifier):
        if not identifier in self.pool:
            self.lock.acquire()
            if not identifier in self.pool: #make sure no other thread got ahead of us in the meantime
                self.pool[identifier] = LockedIotSender(self.myIP)
            self.lock.release()

        anObject = self.pool[identifier]
        anObject.lock.acquire()
        return anObject.IoTSender

    def returnConnectionObj(self, identifier):
        aConnection = self.pool[identifier]
        aConnection.lock.release()


launch_time = None
receiver_enforcement_active = False
myArgs = None
statsPrintTimer = None
totalStatsLastInterval = 0
counterRQokay = fastwritecounter.FastWriteCounter()
counterRQerror = fastwritecounter.FastWriteCounter()
counterRQRelayed = fastwritecounter.FastWriteCounter()
theSenderPool = None
inRelayMode = False


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
                 print("###### RECEIVER ENFORCEMENT IS NOW ACTIVE ######")

        while True:

            global counterRQerror
            global counterRQokay
            global inRelayMode

            if receiver_enforcement_active:
                if inRelayMode:
                    allowedList = global_settings.authorized_senders_terminal
                else:
                    allowedList = global_settings.authorized_senders

                if not self.client_address[0] in allowedList:
                    print("Rejecing {0}, not on list of authorized senders.".format(self.client_address[0]))
                    #counterRQerror.increment() #Not counting this as an error for now
                    self.request.sendall(bytes(global_settings.status_code_server_error, global_settings.comms_encoding))
                    return #leave function to kill off connection after rejection message

            self.data = str(self.request.recv(global_settings.comms_chunk_size).strip(),global_settings.comms_encoding)
            #print("{0} wrote: {1}".format(self.client_address[0], self.data))

            if (self.data == global_settings.status_code_rq_done):
                return #Leave function, we're done here

            if not validator.validateInput(self.data):
                try:
                    self.request.sendall(bytes(global_settings.status_code_input_invalid, global_settings.comms_encoding))
                except:
                    pass #Very little we can do at this point and I don't feel like spending the time to parse out the different error states
                finally:
                    counterRQerror.increment()
            else:
                if not myArgs.isrelay:
                    counterRQokay.increment()
                else:
                    #print("Relaying Data...")
                    global theSenderPool
                    global counterRQRelayed
                    clientAddr = self.client_address[0]
                    try:
                        sender_obj = theSenderPool.getIoTSender(clientAddr)
                        sender_obj.sendData(self.data)
                        counterRQRelayed.increment()
                    except:
                        #print("Failed to send data to relay. Skipping.")
                        counterRQerror.increment()
                    finally:
                        theSenderPool.returnConnectionObj(clientAddr)
                
                self.request.sendall(bytes(global_settings.status_code_ok, global_settings.comms_encoding))

def printStats():
    global counterRQokay
    global counterRQerror
    global counterRQRelayed
    global launch_time
    global totalStatsLastInterval

    time_passed = (time.time() - launch_time)
    rqOkay = counterRQokay.value()
    rqError = counterRQerror.value()
    rqRelayed = counterRQRelayed.value()
    requests_total = rqOkay + rqError + rqRelayed

    requestPerSec = (requests_total - totalStatsLastInterval) / global_settings.statsPrintInterval
    totalStatsLastInterval = requests_total

    print("{time},{total},{per_sec},{okay},{relayed},{error}".format(time=time_passed,total=requests_total,per_sec=requestPerSec,okay=rqOkay,relayed=rqRelayed,error=rqError))

    statsPrintTimer = threading.Timer(global_settings.statsPrintInterval, printStats)
    statsPrintTimer.start()



if __name__ == "__main__":
    myArgs = arg_parse()
    random.shuffle(global_settings.peer_nodes)

    statsPrintTimer = threading.Timer(global_settings.statsPrintInterval, printStats)
    statsPrintTimer.start()

    inRelayMode = (myArgs.isrelay == 1)

    if inRelayMode:
        theSenderPool =  lockedIotSenderPool(myIP = myArgs.localip)
        print("Operating in RELAY mode.")
    else:
        print("Operating in TERMINAL mode.")

    with myCustomServer((global_settings.server_bind, global_settings.comms_port), iotHandler) as server:
        print ("Starting server on {0}:{1}".format(global_settings.server_bind, global_settings.comms_port))
        launch_time = time.time()
        print("Seconds since Launch,Total Requests,Requests Per Sec,Requests Okay,Requests Relayed,Requests Error")
        server.serve_forever()
