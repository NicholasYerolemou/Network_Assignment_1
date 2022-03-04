class Message:
    # dict filled with default values
    msg = {"ID": -1, "IP": "127.0.0.1", "pin": 0, "data": ""}

    # used when decoding a datagram sent to you
    # the full datagram sent to the server is passed here as a string
    def __init__(self, datagram, code):
        if(code == "decode"):
            words = datagram.split()  # splits the datagram into seperate words seperated by a space
            list_iterator = iter(words)  # creates an iterator over the array
            self.msg["ID"] = int(words[0])  # adds the ID to the dict
            # moves to the second item in the iterator i.e. skipping the word that held ID
            next(list_iterator)
            self.msg["IP"] = words[1]
            next(list_iterator)

            for word in list_iterator:  # loops through the left over words and places them into data
                self.msg["data"] = self.msg["data"] + word

        else:
            if "ID" in datagram:
                self.msg["ID"] = datagram["ID"]
            if "IP" in datagram:
                self.msg["IP"] = datagram["IP"]
            if "pin" in datagram:
                self.msg["pin"] = datagram["pin"]
            if "data" in datagram:
                self.msg["data"] = datagram["data"]

    def getID(self):
        return self.msg["ID"]

    def getData(self):
        return self.msg["data"]

    def getIP(self):
        return self.msg["IP"]

    def getPin(self):
        return self.msg["pin"]

    def toString(self):  # returns a string of each item in the dict
        print("toString method called")
        output = ""
        for key in self.msg:
            output = output + str(self.msg[key]) + " "
        output = output.strip()
        return output
