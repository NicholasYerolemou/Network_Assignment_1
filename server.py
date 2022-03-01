from socket import *

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM)  # creates socket
# assigns the given port number to the servers socket
serverSocket.bind(('', serverPort))

print("The server is ready to recieve")

while True:  # waits for a packet to arrive
    # recives packet and client address (IP,port number)
    message, clientAddress = serverSocket.recvfrom(2048)
    modifiedMessage = message.decode().upper()  # puts the message in upper case
    # sends it back to the client
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
    # socket stays open and listening for more packets
