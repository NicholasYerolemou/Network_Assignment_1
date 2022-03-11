from Message import *


class Chat:
    chatHistory = []  # [[IP,message] [IP,message]]
    members = []
    msg = Message("", "")
    chatId = 0

    def __init__(self, chatId, IPs):
        self.chatId = chatId
        self.members = IPs

    def getChatHistory(self):
        #Returns chat history
        output = ""
        prevIP = ""
        counter = 1

        #Loops through IP and message sent
        for i in self.chatHistory:
            stuff = ""
            ip = i[0] #Gets IP address
            data = i[1]

            #If IP messages multiple times in a row, stores IP once and messages one after each other
            if (ip == prevIP):
                stuff = stuff + "," + i[1]
                output = output + stuff
                prevIP = ip
            else:
                stuff = i[1]
                output = output + "_" + ip + ":" + stuff
                counter = 0
                prevIP = ip
        return output[1:]


    def getID(self):
        #Returns chat ID
        return self.chatId

    def getIPs(self):
        #Returns members of the chat
        return self.members

    def addMessage(self, ip, data):
        #Adds a message to the chat history
        if(data != ""):
            self.chatHistory.append([ip, data])

    def addMember(self, ip):
        #Adds a member to the chat
        self.members.append(ip)

    def clearChatHistory(self):
        #Clears chat history
        self.chatHistory = []

    def removeMember(self, ip):
        #Removes member from chat
        self.members.remove(ip)

    # def addMessage(self, ipAddress , msg):
