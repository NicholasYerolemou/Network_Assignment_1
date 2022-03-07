from Message import *


class Chat:
    chatHistory = [[], []]
    members = []
    msg = Message("", "")
    chatId = 0

    def __init__(self, chatId, IPs):
        self.chatId = chatId
        members = IPs

    def getChatHistory(self, chatId):
        return self.chatHistory

    def getID(self):
        return self.chatId

    def getIPs(self):
        return self.members

    # def addMessage(self, ipAddress , msg):
