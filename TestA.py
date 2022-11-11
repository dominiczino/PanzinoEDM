import zmq
import time

context = zmq.Context()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response

for request in range(10):
    print("Sending request %s …" % request)
    socket.send(b"Hello")

    #  Get the reply.
    message=None
    while message is None:
        try:
            message = socket.recv(flags=zmq.NOBLOCK)
        except:
            print("WELL!?!?!? WE'RE WAITING")
            
    print("Received reply %s [ %s ]" % (request, message))
