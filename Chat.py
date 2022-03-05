from Message import *
class Chat:
    chatHistory = [[],[]]
    ipAddress = ""
    memberIps = []
    msg = Message("","")
    chatId = 0
    def __init__(self,chatId):
        self.chatId = chatId


    def getChatHistory(self,chatId):
        return self.chatHistory

    def getChatId(self):
        return self.chatId

    #def addMessage(self, ipAddress , msg):

