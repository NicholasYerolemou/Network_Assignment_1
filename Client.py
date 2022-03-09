from socket import *
import tkinter as tk
from tkinter import messagebox
import threading
from Message import Message
import sys
import select


serverName = "127.0.0.1"  # set the servers IP address
serverPort = 12005  # server port number
server = (serverName, serverPort)
chats = []

serverWindow = tk.Tk()
serverWindow.title("ServerConnect")
serverWindow.geometry("350x100")
serverWindow.configure(bg='WHITE')


lblWelcome = tk.Label(serverWindow, text="Hello!", font=(
    'Helvatical bold', 15), bg='WHITE', fg='#a83f2c').pack(side=tk.TOP)
lblName = tk.Label(serverWindow, text="Please enter your name.", font=(
    'Helvatical bold', 10), bg='WHITE', fg='#a83f2c').pack(side=tk.TOP)
lblName = tk.Label(serverWindow, text="YOUR NAME:",
                   bg='WHITE').pack(side=tk.LEFT)
entName = tk.Entry(serverWindow, bg='WHITE')
entName.pack(side=tk.LEFT)


btnConnect = tk.Button(serverWindow, text="CONNECT", bg='WHITE',
                       width=20, command=lambda: connectServer(entName.get()))
btnConnect.pack(side=tk.LEFT)


def connectServer(name):  # connects the client to the server
    global Name, client
    if len(name) < 1:
        tk.messagebox.showerror(
            title="ERROR!!!", message="Please enter your name. <e.g. John>")
    else:
        Name = name
        menu(serverWindow)


def menu(window):
    window.destroy()
    window = tk.Tk()
    window.title("MAIN MENU")

    window.geometry("500x500")
    window.configure(bg='WHITE')

    lblWelcome = tk.Label(window, text="WELCOME!", font=(
        'Helvatical bold', 30), bg='WHITE', fg='#a83f2c').pack(side=tk.TOP)
    lblOption = tk.Label(window, text="Please select an option:", font=(
        'Helvatical bold', 20), bg='WHITE', fg='#a83f2c').pack(side=tk.TOP)

    btnCreateChat = tk.Button(window, text="START NEW CHAT", width=200, height=5, bg='#a83f2c', fg='WHITE', font=(
        'Helvatical bold', 15), command=lambda: newChat(window))
    btnCreateChat.pack(side=tk.TOP)

    btnOpenChat = tk.Button(window, text="OPEN EXISTING CHAT", width=200, height=5, bg='#a83f2c',
                            fg='WHITE', font=('Helvatical bold', 15), command=lambda: openChat(window))
    btnOpenChat.pack(side=tk.TOP)

    btnExit = tk.Button(window, text="EXIT", width=200, height=5, bg='#a83f2c', fg='WHITE', font=(
        'Helvatical bold', 15), command=lambda:  exitApp(window))
    btnExit.pack(side=tk.TOP)


def newChat(window):
    window.destroy()
    temp = {"ID": 2}
    msg = Message(temp, "encode")
    # creates a new chat with the server with just the client in
    sock.sendto(msg.toString().encode(), server)
    packet, serverName = sock.recvfrom(2048)
    msg = Message(packet.decode(), "decode")
    # adds the new chat ID to out list of existing chats
    chats.append(msg.getChatID())

    newChat = tk.Tk()
    newChat.title("NewChat")

    newChat.geometry("500x500")

    topFrame = tk.Frame(newChat)
    topFrame.pack(side=tk.TOP)

    btnBack = tk.Button(topFrame, text="RETURN",
                        command=lambda: returnToMain(newChat))
    btnBack.pack(side=tk.LEFT)

    lblIP = tk.Label(topFrame, text="Their IP:").pack(side=tk.LEFT)
    entIP = tk.Entry(topFrame)
    entIP.pack(side=tk.LEFT)

    btnAddUser = tk.Button(topFrame, text="ADD PARTICIPANT", command=lambda: disable(
        entIP, chats[-1], btnConnect, tkMessage))
    btnAddUser.pack(side=tk.LEFT)

    btnExit = tk.Button(topFrame, text="EXIT",
                        command=lambda: exitApp(newChat))
    btnExit.pack(side=tk.RIGHT)

    displayFrame = tk.Frame(newChat)
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

    bottomFrame = tk.Frame(newChat)
    tkMessage = tk.Text(bottomFrame, height=2, width=55)
    tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
    tkMessage.config(highlightbackground="grey", state="disabled")
    chatHistory = []
    tkMessage.bind("<Return>", (lambda event: getChatMessage(
        tkMessage.get("1.0", tk.END), chats[-1], tkDisplay, tkMessage, newChat)))
    bottomFrame.pack(side=tk.BOTTOM)


def getChatMessage(input, chatID, display, message, window):
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
        output = i[0]  # the IP address
        for word in i[1]:
            output = output + "\n" + word
    print(output)

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
    window.destroy()
    openChat = tk.Tk()
    openChat.title("OpenChat")

    openChat.geometry("500x500")
    content = {"ID": 8}
    msg = Message(content, "encode")
    sock.sendto(msg.toString().encode(), server)

    packet, serverName = sock.recvfrom(2048)
    msg = Message(packet.decode(), "decode")
    data = msg.getData()
    temp = data.split()
    chatID = 0
    # 2d array holds chat id and ips in format [('1', ['123', '1234', '234']), ('2', ['1234', '1234', '231412'])]
    chats = []
    for t in temp:
        parts = t.split(":")
        chatID = parts[0]  # gets the stuff on the left side of the colon
        chatIPS = parts[1].split(",")
        temp = (chatID, chatIPS)
        chats.append(temp)
    displayFrame = tk.Frame(openChat)
   # btnExit = tk.Button(displayFrame, text="EXIT", command=lambda: exitApp(openChat))
   # btnExit.pack(side=tk.LEFT)
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

    update_chat_list(chats, tkDisplay)

    bottomFrame = tk.Frame(openChat)
    lblHeading = tk.Label(
        bottomFrame, text="Type the number of the chat you'd like to open:").pack(side=tk.LEFT)
    chatNum = tk.Entry(bottomFrame)
    chatNum.pack(side=tk.LEFT)

    btnOpen = tk.Button(bottomFrame, text="OPEN CHAT",
                        command=lambda: openSpecificChat(chatID, openChat))

    btnOpen = tk.Button(bottomFrame, text="OPEN CHAT",
                        command=lambda: openSpecificChat(chatNum.get(), openChat))
    btnOpen.pack(side=tk.RIGHT)
    bottomFrame.pack(side=tk.TOP)


def update_chat_list(names, tkDisplay):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in names:
        display = "ChatID:", c[0], " Members:", c[1], "\n"
        tkDisplay.insert(tk.END, display)
    tkDisplay.config(state=tk.DISABLED)


def openSpecificChat(chatID, window):
    window.destroy()

    newChat = tk.Tk()
    newChat.title("NewChat")

    newChat.geometry("500x500")

    topFrame = tk.Frame(newChat)
    topFrame.pack(side=tk.TOP)

    btnBack = tk.Button(topFrame, text="RETURN",
                        command=lambda: returnToMain(newChat))
    btnBack.pack(side=tk.LEFT)

    lblIP = tk.Label(topFrame, text="Their IP:").pack(side=tk.LEFT)
    entIP = tk.Entry(topFrame)
    entIP.pack(side=tk.LEFT)

    btnAddUser = tk.Button(topFrame, text="ADD PARTICIPANT", command=lambda: disable(
        entIP, chats[-1], btnConnect, tkMessage))
    btnAddUser.pack(side=tk.LEFT)

    btnExit = tk.Button(topFrame, text="EXIT",
                        command=lambda: exitApp(newChat))
    btnExit.pack(side=tk.RIGHT)

    displayFrame = tk.Frame(newChat)
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

    bottomFrame = tk.Frame(newChat)
    tkMessage = tk.Text(bottomFrame, height=2, width=55)
    tkMessage.pack(side=tk.LEFT, padx=(5, 13), pady=(5, 10))
    tkMessage.config(highlightbackground="grey", state="disabled")
    tkMessage.bind("<Return>", (lambda event: getChatMessage(
        tkMessage.get("1.0", tk.END), tkDisplay, tkMessage, newChat)))
    bottomFrame.pack(side=tk.BOTTOM)

    content = {"ID": 9, "chatID": chatID}
    msg = Message(content, "encode")
    sock.sendto(msg.encode(), server)  # requests chat history

    pakcet, serverName = sock.recvfrom(2048)
    msg = Message(packet, "decode")

    # print this to the screen
    chatHistory = getChatHistory(msg)


def getChatHistory(msg):
    chatHistory = []
    # data in format [('127.0.0', ['hello', 'how are you', ' sttsfd']), ('123232.123', ['afadsfa', 'asdfasf', 'adfas'])
    items = msg.getData().split("_")

    for item in items:
        parts = item.split(":")
        ip = parts[0]
        messages = parts[1].split(",")
        temp = (ip, messages)
        chatHistory.append(temp)
    return chatHistory


def disable(entIP, chatID, btnConn, tkMessage):  # adds a user to a specific chat
    global ip, client

    if len(entIP.get()) < 1:
        tk.messagebox.showerror(
            title="ERROR!!!", message="You MUST enter the IP address of the person you wish to chat with <e.g. 203.0.113.42>")
    else:
        entIP.config(state=tk.DISABLED)
        tkMessage.config(state=tk.NORMAL)
        connectUser(chatID, entIP)


def connectUser(chatID, entIP):
    content = {"ID": 5, "chatID": chatID, "data": str(entIP.get())}
    msg = Message(content, "encode")
    sock.sendto(msg.toString().encode(), server)

    entIP.config(state=tk.NORMAL)


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
    except:  # connection attemp timed out
        return False

    return False


with socket(AF_INET, SOCK_DGRAM) as sock:
    sock.settimeout(0.1)

    connected = False

    while(not connected):  # connect to server
        connected = connectToServer()
    print("connected")
    serverWindow.mainloop()
    # we have succesfully connected to the server

    while True:
        while True:
            # print("checking for recieved messages")
            try:
                packet, serverAddress = sock.recvfrom(2048)
                message = Message(packet.decode(), "decode")

                processPacket(message)  # a messages was recieved process it
            except:  # socket.timeout(): fix that later so it excepts a specific exception rather than all
                # print("no messages recieved \n")
                break
        # waits 5 seconds for user input
        print("waiting for user input ...")
        # type NC ip ip ip ...
        i, o, e = select.select([sys.stdin], [], [], 10)
        if(i):
            input = sys.stdin.readline()
            processInput(input)

    sock.close()
