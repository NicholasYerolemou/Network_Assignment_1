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


with socket(AF_INET, SOCK_DGRAM) as sock:
    content = {"ID": 0}
    msg = Message(content, "encode")
    sock.sendto(msg.toString().encode(), server)
    packet, serverAddress = sock.recvfrom(2048)
    message = Message(packet.decode(), "decode")
    processPacket(message)

    sock.close()
