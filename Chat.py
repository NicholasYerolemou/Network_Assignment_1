class Chat:
    def __init__(self,chatHistory,chatId):
        self.chatHistory = chatHistory
        self.chatId = chatId

    def getChatHistory(self,Id):
        return self.chatHistory