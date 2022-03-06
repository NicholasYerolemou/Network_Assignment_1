from socket import *
from Message import Message
from Chat import *
from collections import OrderedDict

port = 12005
host = "127.0.0.1"
connected = {}
chats = OrderedDict()


def isConnected(IP):
    if(IP in connected):
        return True
    else:
        return False


"""
def notifyChatMembers(chat):
    members = chat.get
    for mem in members:
        if(isConnected(mem)):
            target = (mem, connected[mem])
            data = str("You have been added to chat number:",
            content = {"ID": 3, "IP": "127.0.0.1", "pin": 0, "data":}
            msg=Message()
            sock.sendto(msg.toString().encode(), target)
"""


def getConnectedClients(IPs):
    temp = []
    for ip in IPs:
        if ip in connected:
            temp2 = (ip, connected[ip])
            temp.append(temp2)

    return temp


def processPacket(msg, client):
    id = msg.getID()
    if(id == 0):  # send back ack response
        print("Connected to client with IP:", client[0], "on port:", client[1])
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

    elif(id == 1):
        print("code is 1")
    elif(id == 2):
        print("Chat created")
        # make new chat
        # the data contains all the IPs of the clients added to the chat
        members = msg.getData().split()  # gets IP addresses stored in data
        size = len(chats)
        chatID = 0
        if(len(chats) == 0):  # if no chats currently exist
            chatID = 1
            temp = {chatID: Chat(chatID, members)}
            chats.update(temp)
        else:
            # get the most recent chat id and add 1 to it
            # chatID = chats[size-1].getID() + 1
            temp = list(chats.keys())
            chatID = temp[-1] + 1
            temp = {chatID: Chat(chatID, members)}
            chats.update(temp)

        # send a message to all connected clients they have been added to a chat
        clientsToNotify = getConnectedClients(members)
        for client in clientsToNotify:
            reply = {"ID": 2, "chatID": chatID}
            msg = Message(reply, "encode")
            sock.sendto(msg.toString().encode(), client)

    elif(id == 3):  # might need fixing
        ports = connected[msg.getIP()]
        if client[1] == ports[0]:
            target = (msg.getIP(), ports[1])
        else:
            target = (msg.getIP(), ports[0])
        sock.sendto(msg.toString().encode(), target)
    elif(id == 4):
        print("end chat")
    elif(id == 5):
        print("add participant")
    elif(id == 6):
        del connected[client[0]]  # removes user from connect dict
    elif(id == 7):
        print("leave chat")

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
