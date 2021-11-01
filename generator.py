import random
import time
import os
import uuid
import global_settings
import sender

class iotGenerator:
    def __init__(self):
        self.currentCurveStep = global_settings.curveStep
        self.senderObj = sender.iotDataSender()

    def generateValue(self):
        self.currentCurveStep += 1
        simulationVal = random.randrange( (global_settings.curveStep % global_settings.curveMod) * global_settings.rotAmplifier, global_settings.curveCeiling)
        if simulationVal < global_settings.curveFloor:
            simulationVal = global_settings.curveFloor
        return global_settings.data_format.format(id=global_settings.node_identifier, value=str(simulationVal))

    def generateSendSleep(self):
        simulationVal = self.generateValue()
        self.senderObj.sendData(simulationVal)
        #print("Sent: " + simulationVal)
        time.sleep(random.randrange(global_settings.sleepMin, global_settings.sleepMax) / global_settings.sleepDivide)

def main():
    theGenerator = iotGenerator()

    while True:
        theGenerator.generateSendSleep()

if __name__=="__main__":
    main()

