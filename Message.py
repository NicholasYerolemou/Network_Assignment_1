class Message:
    # dict filled with default values
    msg = {"ID": -1, "chatID": 0, "pin": 0, "data": ""}

    # used when decoding a datagram sent to you
    # the full datagram sent to the server is passed here as a string

    def __init__(self, datagram, code):
        msg = {"ID": -1, "IP": ["127.0.0.1"],
               "chatID": 0, "pin": 0, "data": ""}

        if(code == "decode"):
            words = datagram.split()  # splits the datagram into seperate words seperated by a space
            list_iterator = iter(words)  # creates an iterator over the array

            self.msg["ID"] = int(words[0])  # adds the ID to the dict
            next(list_iterator)

            self.msg["chatID"] = int(words[1])
            next(list_iterator)

            self.msg["pin"] = int(words[2])
            next(list_iterator)

            for word in list_iterator:  # loops through the left over words and places them into data
                self.msg["data"] = self.msg["data"] + word

        else:
            if "ID" in datagram:
                self.msg["ID"] = datagram["ID"]
            if "IP" in datagram:
                self.msg["chatID"] = datagram["chatID"]
            if "pin" in datagram:
                self.msg["pin"] = datagram["pin"]
            if "data" in datagram:
                self.msg["data"] = datagram["data"]

    def getID(self):
        return self.msg["ID"]

    def getData(self):
        return self.msg["data"]

    def getchatID(self):
        return self.msg["chatID"]

    def getPin(self):
        return self.msg["pin"]

    def toString(self):  # returns a string of each item in the dict
        output = ""
        for key in self.msg:
            output = output + str(self.msg[key]) + " "
        output = output.strip()
        return output
