from socket import *
from Message import Message


port = 12000
host = "127.0.0.1"


def processPacket(msg, client):
    id = msg.getID()
    if(id == 0):  # send back ack response
        print("Connected to client")
        reply = {"ID": 1}
        msg = Message(reply, "encode")
        sock.sendto(msg.toString().encode(), client)
    elif(id == 3):
        print("messaged recieved from client")
        targetClient = (msg.getIP(), 12000)  # create new person to send to
        stuff = msg.toString()
        # print(stuff)
        sock.sendto(stuff.encode(), (msg.getIP(), 12000))
    else:
        print("error")


with socket(AF_INET, SOCK_DGRAM) as sock:
    sock.bind((host, port))
    print("Server ready to recive ...")
    while True:
        print("Server ready to recive ...")
        packet, clientAddress = sock.recvfrom(2048)
        # creates a message object with the data
        message = Message(packet.decode(), "decode")
        # print(packet.decode())
        processPacket(message, clientAddress)
