#   Snoopy.py
#   Dominic Panzino
#   Heartbeat Monitor and Thingsboard Client

import time
import requests
import json
import zmq
import os


with open("Snoopy.json","r") as configFile:
    CONFIGURATION=json.loads(configFile.read())

context = zmq.Context()
socket=context.socket(zmq.REP)
socket.bind("tcp://*:{}".format(CONFIGURATION["INTERNAL_PORT"]))

status={"HEARTBEAT_Thingsboard":0}


RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'
def colorPrint(msg,colorCode):
    print(colorCode+msg+NC)


def PostStatus():
    r=requests.post("http://24.112.137.204:8080/api/v1/{}/telemetry".format("VNusaO33hPUhJ80USdx7"), json={"ts":int(time.time()*1000),"values":status})
    if r.status_code==200:
        excessTime=max(CONFIGURATION["POST_PERIOD"]-CONFIGURATION["DEAD_TIMEOUT"],0.25) #This weird thing makes sure Thingsboard doesn't get tagged as dead just because it updates less frequently
        status.update({"HEARTBEAT_Thingsboard":time.time()+excessTime})

def DisplayStatus():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("SYSTEM STATUS")
    for key in status:
        if "HEARTBEAT_" in key:
            print(key[10:],end=" -")
            for i in range(25-len(key)):
                print("-",end="")
            print("> ",end="")
            if time.time()-status[key] > CONFIGURATION["DEAD_TIMEOUT"]:
                colorPrint("DEAD",RED)
            else:
                colorPrint("ONLINE",GREEN)

lastPostTime=0
lastDisplayTime=0
while True:
    try:
        message = str(socket.recv(flags=zmq.NOBLOCK),encoding="ascii")
        socket.send(b"ack")
        status.update(json.loads(message)) #appends any data from the message into our own status dictionary
    except zmq.error.Again: #This error is thrown any time there is no message waiting to be read
        if time.time()-lastPostTime>CONFIGURATION["POST_PERIOD"]:
            PostStatus()
            lastPostTime=time.time()
        if time.time()-lastDisplayTime>CONFIGURATION["DISPLAY_PERIOD"]:
            DisplayStatus()
            lastDisplayTime=time.time()
        
    except Exception as oof:
        colorPrint("Something has gone terribly wrong...",RED)
        colorPrint(oof,RED)
