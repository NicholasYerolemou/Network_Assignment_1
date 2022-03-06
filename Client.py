from socket import *
from Message import Message
import sys
import select
import termios

serverName = "127.0.0.1"  # set the servers IP address
serverPort = 12005  # server port number
server = (serverName, serverPort)


def processPacket(msg):
    if(msg.getID() == 1):
        print("connected to server\n")
    elif(msg.getID() == 2):
        print("create chat")
    elif(msg.getID() == 3):
        print("A user said", msg.getData())
    elif(msg.getID() == 4):
        print("end chat")
    elif(msg.getID() == 5):
        print("add participant")
    elif(msg.getID() == 6):
        print("request chat list")
    elif(msg.getID() == 7):
        print("leave chat")


def processInput(input):
    content = {"ID": 3, "IP": "127.0.0.1", "pin": 1, "data": input}
    msg = Message(content, "encode")
    sock.sendto(msg.toString().encode(), server)


def connectToServer():
    content = {"ID": 0}
    msg = Message(content, "encode")
    sock.sendto(msg.toString().encode(), server)
    try:
        packet, serverAddress = sock.recvfrom(2048)
        message = Message(packet.decode(), "decode")
        if(message.getID() == 1):
            return True
    except:  # connection attemp timed out
        return False

    return False


with socket(AF_INET, SOCK_DGRAM) as sock:
    sock.settimeout(0.1)

    connected = False

    while(not connected):  # connect to server
        connected = connectToServer()
    # we have succesfully connected to the server
    while True:
        while True:
            #print("checking for recieved messages")
            try:
                packet, serverAddress = sock.recvfrom(2048)
                message = Message(packet.decode(), "decode")

                processPacket(message)  # a messages was recieved process it
            except:  # socket.timeout(): fix that later so it excepts a specific exception rather than all
                #print("no messages recieved \n")
                break
        # waits 5 seconds for user input
        print("waiting for user input ...")
        i, o, e = select.select([sys.stdin], [], [], 5)
        if(i):
            input = sys.stdin.readline()
            processInput(input)

    sock.close()
