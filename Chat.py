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
        output = ""
        prevIP = ""
        counter = 1

        for i in self.chatHistory:
            stuff = ""
            ip = i[0]
            data = i[1]

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
        return self.chatId

    def getIPs(self):
        return self.members

    def addMessage(self, ip, data):
        if(data != ""):
            self.chatHistory.append([ip, data])

    def addMember(self, ip):
        self.members.append(ip)

    def clearChatHistory(self):
        self.chatHistory = []

    def removeMember(self, ip):
        self.members.remove(ip)

    # def addMessage(self, ipAddress , msg):
