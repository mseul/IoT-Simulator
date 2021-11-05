import random
import time
import os
import uuid
import global_settings
import sender
import codecs
import random

import argparse

def arg_parse():
    theParser = argparse.ArgumentParser(description="IoT Simulator")
    theParser.add_argument("--localip", dest="localip", action="store", required=True)
    theParser.add_argument("--nodename", dest="nodename", action="store", required=True)
    return theParser.parse_args()


class iotGenerator:
    def __init__(self):
        self.currentCurveStep = global_settings.curveStep
        self.myArgs = arg_parse()
        self.senderObj = sender.iotDataSender(myIP = self.myArgs.localip)

    def generateValue(self):
        self.currentCurveStep += 1

        simulationVal = random.randrange( (global_settings.curveStep % global_settings.curveMod) * global_settings.rotAmplifier, global_settings.curveCeiling)
        if simulationVal < global_settings.curveFloor:
            simulationVal = global_settings.curveFloor

        if global_settings.generator_induce_errors:
            error_decider = random.randrange(global_settings.generator_induced_error_range_floor,global_settings.generator_induced_error_range_ceiling)
            if ( error_decider >= global_settings.generator_induced_error_threshold):
                if (error_decider % 3) == 0: 
                    simulationVal = random.randrange(-100000,-1)
                else:
                    return str(codecs.encode(bytes(str(uuid.uuid4()),"utf-8"),"zip"))

        return global_settings.data_format.format(id=self.myArgs.nodename, value=str(simulationVal))

    def generateSendSleep(self):
        generatedValue = self.generateValue()
        self.senderObj.sendData(generatedValue)
        time.sleep(random.randrange(global_settings.sleepMin, global_settings.sleepMax) / global_settings.sleepDivide)

def main():
    random.shuffle(global_settings.peer_nodes)
    theGenerator = iotGenerator()

    while True:
        theGenerator.generateSendSleep()

if __name__=="__main__":
    main()

