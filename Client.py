from socket import *
from Message import Message
import sys
import select

serverName = "127.0.0.1"  # set the servers IP address
serverPort = 12000  # server port number
server = (serverName, serverPort)


def processPacket(msg):
    if(msg.getID() == 1):
        print("connected to server\n")
    elif(msg.getID() == 2):
        print("create chat")
    elif(msg.getID() == 3):
        print("send message")
        print(msg.getData())
    elif(msg.getID() == 4):
        print("end chat")
    elif(msg.getID() == 5):
        print("add participant")
    elif(msg.getID() == 6):
        print("request chat list")
    elif(msg.getID() == 7):
        print("leave chat")


def processInput(input):
    print("The user entered", input)
    content = {"ID": 3, "IP": "127.0.0.1", "pin": 1, "data": input}
    msg = Message(content, "encode")
    sock.sendto(msg.toString().encode(), server)


with socket(AF_INET, SOCK_DGRAM) as sock:
    sock.settimeout(0.1)
    content = {"ID": 0}
    msg = Message(content, "encode")
    sock.sendto(msg.toString().encode(), server)
    packet, serverAddress = sock.recvfrom(2048)
    message = Message(packet.decode(), "decode")
    processPacket(message)

    while True:
        while True:
            print("checking for recieved messages")
            try:
                packet, serverAddress = sock.recvfrom(2048)
                print("messages recievec")
                message = Message(packet.decode(), "decode")
                processPacket(packet)  # a messages was recieved process it
            except:  # socket.timeout(): fix that later so it excepts a specific exception rather than all
                print("no messages recieved \n")
                break
        # waits 5 seconds for user input
        print("waiting for user input ...")
        i, o, e = select.select([sys.stdin], [], [], 60)
        if(i):  # user typed somehting
            input = sys.stdin.readline()
            processInput(input)
    sock.close()
