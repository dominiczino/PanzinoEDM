#   MotionController.py
#   Dominic Panzino
#   Controls interaction with the Phidgets and has control over most NC operations
#   Recieves commands over TCP port 5556


from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
import time
import zmq
import json




with open("MotionControllerParam.json") as boi:
    P=json.loads(boi.read())


    #Initialize all the sockets we'll need for the communication happening here
context = zmq.Context()
recvSocket=context.socket(zmq.REP)
recvSocket.bind("tcp://*:5556")
snoopySocket=context.socket(zmq.REQ)
snoopySocket.connect("tcp://localhost:5555")
serialSocket=context.socket(zmq.REQ)
serialSocket.connect("tcp://localhost:5557")



X_Phidget=Stepper()
Y_Phidget=Stepper()
Z_Phidget=Stepper()

def initPhidgets():
    if P["X_ENABLE"]:
        X_Phidget.setDeviceSerialNumber(P["X_SERIAL"])
        X_Phidget.openWaitForAttachment(1000)
        X_Phidget.setAcceleration(P["X_ACCEL"])
        X_Phidget.setCurrentLimit(P["X_IDLE_CURRENT"])
        X_Phidget.setEngaged(True)

    if P["Y_ENABLE"]:
        Y_Phidget.setDeviceSerialNumber(P["Y_SERIAL"])
        Y_Phidget.openWaitForAttachment(1000)
        Y_Phidget.setAcceleration(P["Y_ACCEL"])
        Y_Phidget.setCurrentLimit(P["Y_IDLE_CURRENT"])
        Y_Phidget.setCurrentLimit(P["Y_IDLE_CURRENT"])
        Y_Phidget.setEngaged(True)

    if P["Z_ENABLE"]:
        Z_Phidget.setDeviceSerialNumber(P["Z_SERIAL"])
        Z_Phidget.openWaitForAttachment(1000)
        Z_Phidget.setAcceleration(P["Z_ACCEL"])
        Z_Phidget.setCurrentLimit(P["Z_IDLE_CURRENT"])
        Z_Phidget.setEngaged(True)


def homeZ():
    Z_Phidget.setVelocityLimit(P['Z_RAPID']*0.25)
    Z_Phidget.setCurrentLimit(P["Z_HOMING_CURRENT"])
    Z_Phidget.setTargetPosition(P["Z_RANGE"]*-1.1)
    while Z_Phidget.getIsMoving():
        heartbeat()
        time.sleep(0.05)
        



def heartbeat():
    heartbeatJson={"HEARTBEAT_MotionController.py":time.time()}
    snoopySocket.send(bytes(json.dumps(heartbeatJson),"ascii"))
    snoopySocket.recv()


def main():
    heartbeat()


while True:
    main()
