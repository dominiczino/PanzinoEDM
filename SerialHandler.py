#   SerialHandler.py
#   Dominic Panzino
#   Handles serial communication with the Arduino for pulling necessary data
#   Recieves data requests on TCP port 5557


from threading import ExceptHookArgs, excepthook
import zmq
import serial
import serial.tools.list_ports as serialPorts
import time
import json


context=zmq.context()
recvSocket=context.socket(zmq.REP)
recvSocket.bind("tcp://*:5557")
snoopySocket=context.socket(zmq.REQ)
snoopySocket.connect("tcp://localhost:5555")
serialObj=None

dataFromArduino=dict()


def initializeSerialComs():
    try:
        serialObj=serial.Serial("PORT",baudrate=115200,timeout=0.5)
        time.sleep(1)
        return True
    except:
        serialObj.close
        serialObj=None
        heartbeatJson={"HEARTBEAT_ArduinoConnection.py":0}
        snoopySocket.send(bytes(json.dumps(heartbeatJson),"ascii"))
        snoopySocket.recv()
        return False



def refreshData():
    '''Gets a new batch of data from the Arduino'''
    serialObj.write(bytes([1])) # Get spark gap length value
    dataFromArduino["sparkLength"]=int(serialObj.read().hex(),16)

    heartbeatJson={"HEARTBEAT_ArduinoConnection.py":time.time()}
    snoopySocket.send(bytes(json.dumps(heartbeatJson),"ascii"))
    snoopySocket.recv()



def main():
    if serialObj is None:
        success=initializeSerialComs()
    else:
        try:
            message = str(recvSocket.recv(flags=zmq.NOBLOCK),encoding="ascii")
            if message=="GET_STATE":
                recvSocket.send(bytes(json.dumps(dataFromArduino),encoding="ascii"))
            else:
                recvSocket.send(b"ack")

        except zmq.error.Again: #This happens when there is no data to send
            refreshData()





def heartbeat():
    heartbeatJson={"HEARTBEAT_SerialHandler.py":time.time()}
    snoopySocket.send(bytes(json.dumps(heartbeatJson),"ascii"))
    snoopySocket.recv()


while True:
    try:
        main()
    except:
        print("ERROR")