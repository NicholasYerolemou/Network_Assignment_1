from socket import *
from Message import Message
from Chat import *
from collections import OrderedDict
import select
import sys

port = 12007
host = "192.168.0.177"  # "102.39.144.36"
clients = []
chats = OrderedDict()


"""
def isConnected(IP):
    if(IP in connected):
        return True
    else:
        return False
"""

"""
def getConnectedClients(IPs):
    temp = []
    for ip in IPs:
        if ip in connected:
            temp2 = (ip, connected[ip])
            temp.append(temp2)
    return temp
"""


def processPacket(msg, client):
    id = msg.getID()
    if(id == 0):  # send back ack response
        print("Connected to client with IP:", client[0], "on port:", client[1])
        reply = {"ID": 1}
        msg = Message(reply, "encode")
        # add the client to list of connected clients
        if client[0] not in clients:  # if ip address not in clients
            clients.append(client[0])
        sock.sendto(msg.toString().encode(), client)

    elif(id == 1):
        print("code is 1")
    elif(id == 2):
        # make new chat
        # the data contains all the IPs of the clients added to the chat
        # members = msg.getData().split()  # gets IP addresses stored in data
        #size = len(chats)

        members = [client[0]]  # adds just the client to the chat
        chatID = 0
        if(len(chats) == 0):  # if no chats currently exist
            chatID = 1
            chat = Chat(chatID, members)
            temp = {chatID: chat}
            chats.update(temp)
        else:
            # get the most recent chat id and add 1 to it
            temp = list(chats.keys())
            chatID = temp[-1] + 1
            c = Chat(chatID, members)
            temp = {chatID: c}
            chats.update(temp)
            chats[chatID].clearChatHistory()
        # send a message to all connected clients they have been added to a chat
        reply = {"ID": 2, "chatID": chatID}
        msg = Message(reply, "encode")
        sock.sendto(msg.toString().encode(), client)

    elif(id == 3):  # recieved new message
        chatID = msg.getChatID()
        # add the new message to the chat history
        chats[chatID].addMessage(client[0], msg.getData())

        # send back the new chat history
        data = chats[msg.getChatID()].getChatHistory()
        reply = {"ID": 9, "data": data}
        msg = Message(reply, "encode")
        sock.sendto(msg.toString().encode(), client)

    elif(id == 4):
        print("end chat")
    elif(id == 5):
        newUser = msg.getData()
        chatID = msg.getChatID()
        chat = chats[chatID]  # the chat this user should be added to
        newUser = newUser.strip()
        chat.addMember(newUser)

    elif(id == 6):
        del connected[client[0]]  # removes user from connect dict
    elif(id == 7):
        chat = chats[msg.getChatID()]
        chat.removeMember(client[0])

    elif(id == 8):  # returns list of chats this client is in in format chatID:member IP 1, member IP 2
        data = ""
        for key in chats.keys():  # loop through each key in the chats dict
            temp = chats[key]
            IPs = chats[key].getIPs()
            if(client[0] in IPs):  # if the current clients IP is in this chat
                temp = ""
                list_iterator = iter(IPs)
                next(list_iterator)
                temp = IPs[0]
                for IP in list_iterator:
                    temp = temp + "," + IP  # produce comma seperarted list of IPs
                # add chatID: to the front of that list
                temp = str(key) + ":" + temp
                data = data + temp + " "

        reply = {"ID": 8, "data": data}
        msg = Message(reply, "encode")
        sock.sendto(msg.toString().encode(), client)
    elif(id == 9):  # client views a specific chat
        data = chats[msg.getChatID()].getChatHistory()
        reply = {"ID": 9, "data": data}
        msg = Message(reply, "encode")
        sock.sendto(msg.toString().encode(), client)

    else:
        print("error")


with socket(AF_INET, SOCK_DGRAM) as sock:
    sock.bind((host, port))
    print("Server ready to recive ...")
    while True:
        sock.settimeout(2)
        try:
            packet, clientAddress = sock.recvfrom(2048)
            message = Message(packet.decode(), "decode")
            processPacket(message, clientAddress)
        except:
            pass
            # creates a message object with the data

            # print(message.toString())
        i, o, e = select.select([sys.stdin], [], [], 0.1)
        if(i):
            #input = sys.stdin.readline()
            break
    sock.close()
