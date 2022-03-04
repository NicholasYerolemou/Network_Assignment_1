from socket import*
from Message import Message

serverName = "127.0.0.1"  # set the servers IP address
serverPort = 12000  # server port number
server = (serverName, serverPort)


def processPacket(msg):
    if(msg.getID() == 1):
        print("connected to server")
    else:
        print("not connected")
    if(msg.getID() == 2):
        print("create chat")
    if(msg.getID() == 3):
        print("send message")
    if(msg.getID() == 4):
        print("end chat")
    if(msg.getID() == 5):
        print("add participant")
    if(msg.getID() == 6):
        print("request chat list")
    if(msg.getID() == 7):
        print("leave chat")


with socket(AF_INET, SOCK_DGRAM) as sock:
    content = {"ID": 0}
    msg = Message(content, "encode")
    sock.sendto(msg.toString().encode(), server)
    packet, serverAddress = sock.recvfrom(2048)
    message = Message(packet.decode(), "decode")
    processPacket(message)

    sock.close()
