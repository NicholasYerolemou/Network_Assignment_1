from socket import *
import tkinter as tk
from tkinter import messagebox
import threading
from Message import Message
import time

# 192.42.120.238 Cat
# 196.42.86.183 Collins
# 102.39.144.36 nick
serverName = "192.168.0.177"  # set the servers IP address
serverPort = 12007  # server port number
server = (serverName, serverPort)
chats = []

##Creates login window, sets the size and colour
serverWindow = tk.Tk()
serverWindow.title("ServerConnect")
serverWindow.geometry("350x100")
serverWindow.configure(bg='WHITE')
##

##Prints the label and creates a text box to enter name
lblWelcome = tk.Label(serverWindow, text="Hello!", font=('Helvatical bold', 15), bg='WHITE', fg='#a83f2c').pack(side=tk.TOP)
lblName = tk.Label(serverWindow, text="Please enter your name.", font=('Helvatical bold', 10), bg='WHITE', fg='#a83f2c').pack(side=tk.TOP)
lblName = tk.Label(serverWindow, text="YOUR NAME:",bg='WHITE').pack(side=tk.LEFT)
entName = tk.Entry(serverWindow, bg='WHITE')
entName.pack(side=tk.LEFT)
##

##Creates connect button
btnConnect = tk.Button(serverWindow, text="CONNECT", bg='WHITE', width=20, command=lambda: connect(entName.get()))
btnConnect.pack(side=tk.LEFT)
##

##Connects the user to the program
def connect(name):
    global Name, client
    if len(name) < 1: #Checks if the user has entered a name
        tk.messagebox.showerror(title="ERROR!!!", message="Please enter your name. <e.g. John>") #Displays an error message
    else:
        Name = name
        menu(serverWindow)#Opens main menu GUI


##Main menu GUI
def menu(window):
    
    window.destroy()#Closes previous window
    
    ##Creates Main menu window, sets the size and colour
    window = tk.Tk()
    window.title("MAIN MENU")
    window.geometry("500x500")
    window.configure(bg='WHITE')
    ##

    ##Prints the welcome label and select option text
    lblWelcome = tk.Label(window, text="WELCOME!", font=('Helvatical bold', 30), bg='WHITE', fg='#a83f2c').pack(side=tk.TOP)
    lblOption = tk.Label(window, text="Please select an option:", font=('Helvatical bold', 20), bg='WHITE', fg='#a83f2c').pack(side=tk.TOP)
    ##

    ##Creates the main menu buttons
    btnCreateChat = tk.Button(window, text="START NEW CHAT", width=200, height=5, bg='#a83f2c', fg='WHITE', font=('Helvatical bold', 15), command=lambda: newChat(window))#Creates a new chat
    btnCreateChat.pack(side=tk.TOP)
    btnOpenChat = tk.Button(window, text="OPEN EXISTING CHAT", width=200, height=5, bg='#a83f2c',fg='WHITE', font=('Helvatical bold', 15), command=lambda: openChat(window))#Opens the page of existing chats
    btnOpenChat.pack(side=tk.TOP)
    btnExit = tk.Button(window, text="EXIT", width=200, height=5, bg='#a83f2c', fg='WHITE', font=('Helvatical bold', 15), command=lambda:  exitApp(window))#Exits program
    btnExit.pack(side=tk.TOP)
    ##
##End of menu() method

##New chat GUI
def newChat(window):
    ##Opens a new chat and allows the user to add participants and send messages
    
    window.destroy()#Closes previous window
    
    ##Creates a new chat with the server with just the client in
    temp = {"ID": 2}
    msg = Message(temp, "encode")
    sock.sendto(msg.toString().encode(), server)
    packet, serverName = sock.recvfrom(2048)
    msg = Message(packet.decode(), "decode")
    chats.append(msg.getChatID())# adds the new chat ID to out list of existing chats
    ##

    ##Creates the new chat window, sets the size
    newChat = tk.Tk()
    newChat.title("NewChat")
    newChat.geometry("500x500")
    ##

    ##Creates top frame
    topFrame = tk.Frame(newChat)
    topFrame.pack(side=tk.TOP)
    ##

    ##Creates return and exit buttons
    btnBack = tk.Button(topFrame, text="RETURN",command=lambda: returnToMain(newChat))#Returns to main menu
    btnBack.pack(side=tk.LEFT)
    btnExit = tk.Button(topFrame, text="EXIT",command=lambda: exitApp(newChat))#Exits program
    btnExit.pack(side=tk.RIGHT)
    ##

    ##Creates middle frame
    midFrame = tk.Frame(newChat)
    midFrame.pack(side=tk.TOP)
    ##

    ##Creates add participant label
    lblIP = tk.Label(midFrame, text="ADD PARTICPANT (Enter IP):").pack(side=tk.LEFT)
    entIP = tk.Entry(midFrame)
    entIP.pack(side=tk.LEFT)
    ##

    ##Creates add participant and help button
    btnHelp = tk.Button(midFrame, text="HELP",command=lambda: help())#Opens the help message
    btnHelp.pack(side=tk.RIGHT)
    btnAddUser = tk.Button(midFrame, text="ADD PARTICIPANT", command=lambda: disable(entIP, chats[-1], tkMessage, tkDisplay))#Calls the connectUser method to add a participant to the chat
    btnAddUser.pack(side=tk.LEFT)
    ##
    
    ##Creates display frame for messages in the chat
    displayFrame = tk.Frame(newChat)
    lblLine = tk.Label(displayFrame, text="*********************************************************************").pack()
    scrollBar = tk.Scrollbar(displayFrame)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
    tkDisplay = tk.Text(displayFrame, height=20, width=55)
    tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
    tkDisplay.tag_config("tag_your_message", foreground="blue")
    scrollBar.config(command=tkDisplay.yview)
    tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7",
                     highlightbackground="grey", state="disabled")
    displayFrame.pack(side=tk.TOP)

    bottomFrame = tk.Frame(newChat)
    lblEnterMsg = tk.Label(bottomFrame, text="TYPE YOUR MESSAGE HERE:").pack(side=tk.TOP)
    tkMessage = tk.Text(bottomFrame, height=2, width=55)
    tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
    tkMessage.config(highlightbackground="grey", state=tk.NORMAL)
    tkMessage.bind("<Return>", (lambda event: getChatMessage(
        tkMessage.get("1.0", tk.END), chats[-1], tkDisplay, tkMessage, newChat)))
    bottomFrame.pack(side=tk.BOTTOM)

def help():
    tk.messagebox.showinfo(title="HELP", message="Enter the IP address of the user that you would like to add to the chat and then press the 'ADD PARTICIPANT' button to add them.\nType your message in the text box below and press enter to send it.")
def getChatMessage(input, chatID, display, message, window):
    # get the message the user has tyoed into the new chat
    tkDisplay = display
    tkMessage = message
    input = input.replace('\n', '')
    texts = tkDisplay.get("1.0", tk.END).strip()

    tkDisplay.config(state=tk.NORMAL)

    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete(1.0, tk.END)
    tkDisplay.insert(tk.END, "hello")
    tkDisplay.config(state=tk.DISABLED)

    tkDisplay.see(tk.END)
    tkMessage.delete('1.0', tk.END)

    # this returns the chathistory - print this to the screen

    #print(send_mssage_to_server(input, chatID, window))

    chatHistory = send_mssage_to_server(input, chatID, window)
    output = ""
    for i in chatHistory:
        output = output + i[0]  # the IP address
        for word in i[1]:
            output = output + "\n" + word
        output = output + "\n\n"

    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete(1.0, tk.END)
    tkDisplay.insert(tk.END, str(output))
    tkDisplay.config(state=tk.DISABLED)

    #[(' 127.0.0.1', [' hello',"other messages"])]


def send_mssage_to_server(input, chatID, window):
    content = {"ID": 3, "chatID": chatID, "data": input}
    msg = Message(content, "encode")
    sock.sendto(msg.toString().encode(), server)

    packet, serverName = sock.recvfrom(2048)
    msg = Message(packet.decode(), "decode")
    return getChatHistory(msg)


def returnToMain(window):
    menu(window)


def openChat(window):
    # view existing chats
    window.destroy()
    openChat = tk.Tk()
    openChat.title("OpenChat")

    openChat.geometry("500x500")
    # returns list of chats this client is in in format chatID:member IP 1, member IP 2
    content = {"ID": 8}
    msg = Message(content, "encode")
    sock.sendto(msg.toString().encode(), server)

    packet, serverName = sock.recvfrom(2048)
    msg = Message(packet.decode(), "decode")
    data = msg.getData()
    temp = data.split()
    chats = []
    output = ""
    # 2d array holds chat id and ips in format [('1', ['123', '1234', '234']), ('2', ['1234', '1234', '231412'])]
    for t in temp:
        parts = t.split(":")

        output = output + "\nChat: " + parts[0] + " | Members: "  # add chatID
        # adds the chatID of every chat this client is in to the local list of chatIDs
        chats.append(parts[0])

        temp = parts[1].split(",")
        output = output + temp[0]  # adds the first ip address
        members = ""
        for mem in temp[1:]:  # adds IP addresses
            members = mem + ", " + mem
            if(members != ""):

                output = output + ", " + members #+ "\n"  # adds the ips and chatID together
            else:
                output = output + " " + members #+ "\n"  # adds the ips and chatID together

    # should contain all the chats the client is a part of
    
    topFrame = tk.Frame(openChat)
    btnBack = tk.Button(topFrame, text="RETURN",
                        command=lambda: returnToMain(openChat))
    btnBack.pack(side=tk.LEFT)
    btnExit = tk.Button(topFrame, text="EXIT",
                        command=lambda: exitApp(openChat))
    btnExit.pack(side=tk.RIGHT)
    topFrame.pack(side=tk.TOP)
    displayFrame = tk.Frame(openChat)

    lblLine = tk.Label(
        displayFrame, text="Chat list:\n*********************************************************************").pack()
    scrollBar = tk.Scrollbar(displayFrame)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
    tkDisplay = tk.Text(displayFrame, height=20, width=55)
    tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
    scrollBar.config(command=tkDisplay.yview)
    tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7",
                     highlightbackground="grey", state="disabled")
    displayFrame.pack(side=tk.TOP)

    update_chat_list(output, tkDisplay)

    bottomFrame = tk.Frame(openChat)
    lblHeading = tk.Label(
        bottomFrame, text="ENTER CHAT ID:").pack(side=tk.LEFT)
    chatNum = tk.Entry(bottomFrame)
    chatNum.pack(side=tk.LEFT)

    btnOpen = tk.Button(bottomFrame, text="OPEN CHAT",
                        command=lambda: checkChatNum(chatNum.get(), openChat, chats))
    btnOpen.pack(side=tk.LEFT)
    btnDelete = tk.Button(bottomFrame, text="LEAVE CHAT",
                        command=lambda: deleteChat(chatNum.get()))
    btnDelete.pack(side = tk.RIGHT)
    bottomFrame.pack(side=tk.TOP)

def deleteChat(chatID):
    if(tk.messagebox.askyesno(title="LeaveChat", message="Are you sure you would like to leave chat " + chatID + "?")):
        content = {"ID": 7, "chatID": chatID}
        msg = Message(content, "encode")
        sock.sendto(msg.toString().encode(), server)


def checkChatNum(chatID, window, chats):
    if str(chatID) in chats:
        openSpecificChat(chatID, window)
    else:
        tk.messagebox.showerror(
            title="ERROR!!!", message="Please enter a valid chat ID <e.g. 1>")


def update_chat_list(display, tkDisplay):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)
    tkDisplay.insert(tk.END, display)
    tkDisplay.config(state=tk.DISABLED)


def openSpecificChat(chatID, window):
    window.destroy()

    exChat = tk.Tk()
    exChat.title("ExChat")

    exChat.geometry("500x500")

    topFrame = tk.Frame(exChat)
    topFrame.pack(side=tk.TOP)

    btnBack = tk.Button(topFrame, text="RETURN",
                        command=lambda: openChat(exChat))
    btnBack.pack(side=tk.LEFT)

    btnExit = tk.Button(topFrame, text="EXIT",
                        command=lambda: exitApp(exChat))
    btnExit.pack(side=tk.RIGHT)

    midFrame = tk.Frame(exChat)
    midFrame.pack(side=tk.TOP)

    lblIP = tk.Label(midFrame, text="ADD PARTICIPANT (Enter IP):").pack(side=tk.LEFT)
    entIP = tk.Entry(midFrame)
    entIP.pack(side=tk.LEFT)

    btnAddUser = tk.Button(midFrame, text="ADD PARTICIPANT", command=lambda: disable(
       entIP, chats[-1], tkMessage, tkDisplay))
    btnAddUser.pack(side=tk.LEFT)\
    
    btnHelp = tk.Button(midFrame, text="HELP",
                        command=lambda: help())
    btnHelp.pack(side=tk.RIGHT)

    

    displayFrame = tk.Frame(exChat)
    lblLine = tk.Label(
        displayFrame, text="*********************************************************************").pack()
    scrollBar = tk.Scrollbar(displayFrame)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
    tkDisplay = tk.Text(displayFrame, height=20, width=55)
    tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
    tkDisplay.tag_config("tag_your_message", foreground="blue")
    scrollBar.config(command=tkDisplay.yview)
    tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7",
                     highlightbackground="grey", state="disabled")
    displayFrame.pack(side=tk.TOP)

    bottomFrame = tk.Frame(exChat)
    lblIP = tk.Label(bottomFrame, text="ENTER YOUR MESSAGE HERE:").pack(side=tk.TOP)
    tkMessage = tk.Text(bottomFrame, height=2, width=55)
    tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
    tkMessage.config(highlightbackground="grey", state=tk.NORMAL)
    tkMessage.bind("<Return>", (lambda event: getChatMessage(
        tkMessage.get("1.0", tk.END), chatID, tkDisplay, tkMessage, exChat)))
    bottomFrame.pack(side=tk.BOTTOM)

    content = {"ID": 9, "chatID": chatID}
    msg = Message(content, "encode")
    sock.sendto(msg.toString().encode(), server)  # requests chat history

    packet, serverName = sock.recvfrom(2048)
    msg = Message(packet.decode(), "decode")

    # print this to the screen

    chatHistory = getChatHistory(msg)
    output = ""
    if(chatHistory != []):
        for i in chatHistory:
            output = output + i[0]  # the IP address
            for word in i[1]:
                output = output + "\n" + word
            output = output + "\n\n"
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete(1.0, tk.END)
    tkDisplay.insert(tk.END, str(output))
    tkDisplay.config(state=tk.DISABLED)


def getChatHistory(msg):
    chatHistory = []
    # data in format [('127.0.0', ['hello', 'how are you', ' sttsfd']), ('123232.123', ['afadsfa', 'asdfasf', 'adfas'])
    if(msg.getData()):
        items = msg.getData().split("_")

        for item in items:
            parts = item.split(":")
            ip = parts[0]
            messages = parts[1].split(",")
            temp = (ip, messages)
            chatHistory.append(temp)
    return chatHistory


def disable(entIP, chatID, tkMessage, tkDisplay):  # adds a user to a specific chat
    global ip, client

    if len(entIP.get()) < 1:
        tk.messagebox.showerror(
            title="ERROR!!!", message="You MUST enter the IP address of the person you wish to chat with <e.g. 203.0.113.42>")
    else:
        entIP.config(state=tk.DISABLED)
        tkMessage.config(state=tk.NORMAL)
        connectUser(chatID, entIP, tkDisplay)


def is_valid_IP(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        if int(item) < 0 or int(item) > 255:
            return False
    return True


def connectUser(chatID, entIP, tkDisplay):  # sends message to server to add client to chat
    strEntIp = str(entIP.get())
    if is_valid_IP(strEntIp):
        content = {"ID": 5, "chatID": chatID,
                   "data": str(entIP.get())}  # entIP.get
        msg = Message(content, "encode")
        sock.sendto(msg.toString().encode(), server)
        entIP.config(state=tk.NORMAL)
        output = "\n" + entIP.get() + " has been added.\n"
        entIP.delete(0, tk.END)
        tkDisplay.config(state=tk.NORMAL)
        tkDisplay.insert(tk.END, str(output))
        tkDisplay.config(state=tk.DISABLED)
    else:
        tk.messagebox.showerror(title="ERROR!!!", message="Please enter a valid IP address <e.g. 192.42.120.238>")
        entIP.delete(0, tk.END)
        entIP.config(state=tk.NORMAL)
        tkDisplay.config(state=tk.NORMAL)
        tkDisplay.config(state=tk.DISABLED)


def exitApp(window):
    window.destroy()
    exit(0)


def connectToServer():
    content = {"ID": 0}
    msg = Message(content, "encode")
    sock.sendto(msg.toString().encode(), server)
    try:
        packet, serverAddress = sock.recvfrom(2048)
        message = Message(packet.decode(), "decode")
        if(message.getID() == 1):
            return True
    except:  # connection attempt timed out
        return False

    return False


with socket(AF_INET, SOCK_DGRAM) as sock:
    sock.settimeout(1)

    connected = False
    counter = 0
    while(not connected):  # tries 10 times to connect to server, if not connected sleeps then tries to connect again
        if(counter == 10):
            counter = 0
            print("unable to connect")
            time.sleep(10)
        counter += 1
        connected = connectToServer()
        print("connecting...")
    print("connected")
    sock.settimeout(None)
    serverWindow.mainloop()
    # we have succesfully connected to the server
    sock.close()
