from Message import *


class Chat:
    chatHistory = list()  # [[IP],[message], [IP][message]]
    members = []
    msg = Message("", "")
    chatId = 0

    def __init__(self, chatId, IPs):
        self.chatId = chatId
        self.members = IPs

    def getChatHistory(self):
        output = ""
        prevIP = ""
        output = ""
        for i in self.chatHistory:
            if(i[0] == prevIP):
                output = output + "," + i[1]
                prevIP = i[0]
            else:
                output = "_" + i[0] + ":" + i[1]
                prevIP = i[0]

        return output

    def getID(self):
        return self.chatId

    def getIPs(self):
        return self.members

    def addMessage(self, ip, data):
        self.chatHistory.append([ip, data])

    def addMember(self, ip):
        self.members.append(ip)

    # def addMessage(self, ipAddress , msg):
