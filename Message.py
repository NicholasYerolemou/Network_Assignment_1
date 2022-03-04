class Message:
    msg = {"ID": -1, "data": ""}  # dict filled with default values

    # used when decoding a datagram sent to you
    # the full datagram sent to the server is passed here as a string
    def __init__(self, datagram, code):
        if(code == "decode"):
            words = datagram.split()  # splits the datagram into seperate words seperated by a space
            list_iterator = iter(words)  # creates an iterator over the array
            self.msg["ID"] = int(words[0])  # adds the ID to the dict
            # moves to the second item in the iterator i.e. skipping the word that held ID
            next(list_iterator)

            for word in list_iterator:  # loops through the left over words and places them into data
                self.msg["data"] = self.msg["data"] + word

        else:
            if "ID" in datagram:
                self.msg["ID"] = datagram["ID"]
            if "data" in datagram:
                self.msg["data"] = datagram["data"]

    def getID(self):
        return self.msg["ID"]

    def getData(self):
        return self.msg["data"]

    def toString(self):  # returns a string of each item in the dict
        output = ""
        for key in self.msg:
            output = output + str(self.msg[key]) + " "
        return output
