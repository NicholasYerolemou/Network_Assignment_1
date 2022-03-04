from socket import *
from Message import Message


port = 12000
host = "127.0.0.1"


def processPacket(msg, client):
    id = msg.getID()
    if(id == 0):  # send back ack response
        reply = {"ID": 1}
        msg = Message(reply, "encode")
        sock.sendto(msg.toString().encode(), client)
    else:
        print("error")


with socket(AF_INET, SOCK_DGRAM) as sock:
    sock.bind((host, port))
    print("Server ready to recieve ...")
    while True:
        packet, clientAddress = sock.recvfrom(2048)
        # creates a message object with the data
        message = Message(packet.decode(), "decode")
        processPacket(message, clientAddress)
