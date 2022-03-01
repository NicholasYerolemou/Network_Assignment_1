from socket import*

serverName = "127.0.0.1"  # set the servers IP address
serverPort = 12000  # server port number

# creates client socket. Paramater 1 indicates we are using IPv4. second parameter indicates the socket is of type written. i.e. a UDP socket.
clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input("input lower case sentence:")

# message converted from string type to byte type.
clientSocket.sendto(message.encode(), (serverName, serverPort))
# the message sent from the server  is put into the modified message
# the packtes source address is put into serverAdress. it holds both the IP and port number.
# 2048 is the buffer size
modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

print(modifiedMessage.decode())  # bytes to string
clientSocket.close()
