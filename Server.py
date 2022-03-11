from re import U
from socket import *
from Message import Message
from Chat import *
from collections import OrderedDict
import select
import sys

port = 12007  # port number the server will run on
host = "196.47.244.175"  # IP address the server will run on
clients = []  # the clients that connect
chats = OrderedDict()  # The chatID and asociated chat object for each created chat
IPUserNameMap = dict()  # mapping from IP address to user name


def processPacket(msg, client):
    id = msg.getID()  # the message ID
    if(id == 0):  # Connection request
        print("Connected to client with IP:", client[0], "on port:", client[1])
        # reply to the client with this code to let them know they are connected
        reply = {"ID": 1}
        msg = Message(reply, "encode")
        # add the client to list of clients
        if client[0] not in clients:  # if ip address not in clients
            clients.append(client[0])
        sock.sendto(msg.toString().encode(), client)

    elif(id == 1):
        print("code is 1")
    elif(id == 2):
        # make new chat

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
        for ip in chats[msg.getChatID()].getIPs():
            if(ip in IPUserNameMap):
                data = data.replace(ip, IPUserNameMap[ip])
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
        username = msg.getData()
        username = username.strip(" ")

        if(client[0] in IPUserNameMap):
            IPUserNameMap[client[0]] = username
        else:
            temp = {client[0]: username}
            IPUserNameMap.update(temp)

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
                if(IPs[0] in IPUserNameMap):  # this user has entered a username
                    temp = IPUserNameMap[IPs[0]]
                else:
                    temp = IPs[0]

                for IP in list_iterator:
                    if(IP in IPUserNameMap):
                        temp = temp + "," + IPUserNameMap[IP]
                    else:
                        temp = temp + "," + IP  # produce comma seperarted list of IPs

                # add chatID: to the front of that list
                temp = str(key) + ":" + temp
                data = data + temp + " "
        reply = {"ID": 8, "data": data}
        msg = Message(reply, "encode")
        sock.sendto(msg.toString().encode(), client)
    elif(id == 9):  # client views a specific chat
        data = chats[msg.getChatID()].getChatHistory()
        for ip in chats[msg.getChatID()].getIPs():
            if(ip in IPUserNameMap):
                data = data.replace(ip, IPUserNameMap[ip])
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

        i, o, e = select.select([sys.stdin], [], [], 0.1)
        if(i):
            # input = sys.stdin.readline()
            break
    sock.close()
