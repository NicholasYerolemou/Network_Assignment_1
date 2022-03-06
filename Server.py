from socket import *
from Message import Message


port = 12005
host = "127.0.0.1"
connected = {}


def processPacket(msg, client):
    id = msg.getID()
    if(id == 0):  # send back ack response
        print("Connected to client")
        reply = {"ID": 1}
        msg = Message(reply, "encode")
        # add the client to list of connected clients
        if client[0] in connected:
            # there is onlt 1 client with this IP connected
            if(isinstance(connected[client[0]], int)):
                temp = [connected[client[0]], client[1]]
                connected[client[0]] = temp
                sock.sendto(msg.toString().encode(), client)
            else:
                print("unable to connect 3 clients with the same IP address")

        else:
            temp = {client[0]: client[1]}
            connected.update(temp)
            sock.sendto(msg.toString().encode(), client)

    elif(id == 3):  # might need fixing
        ports = connected[msg.getIP()]
        if client[1] == ports[0]:
            target = (msg.getIP(), ports[1])
        else:
            target = (msg.getIP(), ports[0])
        sock.sendto(msg.toString().encode(), target)
    else:
        print("error")


with socket(AF_INET, SOCK_DGRAM) as sock:
    sock.bind((host, port))
    print("Server ready to recive ...")
    while True:
        packet, clientAddress = sock.recvfrom(2048)
        # creates a message object with the data
        message = Message(packet.decode(), "decode")
        # print(message.toString())
        processPacket(message, clientAddress)
