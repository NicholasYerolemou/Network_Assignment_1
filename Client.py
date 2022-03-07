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

serverWindow = tk.Tk()
serverWindow.title("ServerConnect")
serverWindow.geometry("350x100")
serverWindow.configure(bg='WHITE')


lblWelcome = tk.Label(serverWindow, text="Hello!", font=(
    'Helvatical bold', 15), bg='WHITE', fg='#a83f2c').pack(side=tk.TOP)
lblName = tk.Label(serverWindow, text="Please enter your name\nin order to connect to the server.", font=(
    'Helvatical bold', 10), bg='WHITE', fg='#a83f2c').pack(side=tk.TOP)
lblName = tk.Label(serverWindow, text="YOUR NAME:",
                   bg='WHITE').pack(side=tk.LEFT)
entName = tk.Entry(serverWindow, bg='WHITE')
entName.pack(side=tk.LEFT)


btnConnect = tk.Button(serverWindow, text="CONNECT", bg='WHITE',
                       width=20, command=lambda: connectServer(entName.get()))
btnConnect.pack(side=tk.LEFT)


def connectServer(name):
    global Name, client
    if len(name) < 1:
        tk.messagebox.showerror(
            title="ERROR!!!", message="You MUST enter your name in order to connect to the server <e.g. John>")
    else:
        Name = name
        # connectToServer()
        menu()


def menu():
    serverWindow.destroy()
    window = tk.Tk()
    window.title("MAIN MENU")

    window.geometry("500x500")
    window.configure(bg='WHITE')

    lblWelcome = tk.Label(window, text="WELCOME!", font=(
        'Helvatical bold', 30), bg='WHITE', fg='#a83f2c').pack(side=tk.TOP)
    lblOption = tk.Label(window, text="Please select an option:", font=(
        'Helvatical bold', 20), bg='WHITE', fg='#a83f2c').pack(side=tk.TOP)

    btnCreateChat = tk.Button(window, text="START NEW CHAT", width=200, height=5,
                              bg='#a83f2c', fg='WHITE', font=('Helvatical bold', 15), command=lambda: newChat())
    btnCreateChat.pack(side=tk.TOP)

    btnCreateChat = tk.Button(window, text="OPEN EXISTING CHAT", width=200, height=5,
                              bg='#a83f2c', fg='WHITE', font=('Helvatical bold', 15), command=lambda: openChat())
    btnCreateChat.pack(side=tk.TOP)

    btnCreateChat = tk.Button(window, text="EXIT", width=200, height=5, bg='#a83f2c', fg='WHITE', font=(
        'Helvatical bold', 15), command=lambda:  exitApp())
    btnCreateChat.pack(side=tk.TOP)


def newChat():

    newChat = tk.Tk()
    newChat.title("NewChat")

    newChat.geometry("500x500")

    topFrame = tk.Frame(newChat)
    topFrame.pack(side=tk.TOP)

    lblIP = tk.Label(topFrame, text="Their IP:").pack(side=tk.LEFT)
    entIP = tk.Entry(topFrame)
    entIP.pack(side=tk.LEFT)

    btnConnect = tk.Button(topFrame, text="CONNECT", command=lambda: connect(
        entIP.get(), entIP, btnConnect, tkMessage))
    btnConnect.pack(side=tk.LEFT)

    btnExit = tk.Button(topFrame, text="EXIT", command=lambda: exitApp())
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


def getChatMessage(msg, display, message, window):
    tkDisplay = display
    tkMessage = message
    msg = msg.replace('\n', '')
    texts = tkDisplay.get("1.0", tk.END).strip()

    tkDisplay.config(state=tk.NORMAL)
    if len(texts) < 1:
        tkDisplay.insert(tk.END, "You->" + msg, "tag_your_message")  # no line
    else:
        tkDisplay.insert(tk.END, "\n\n" + "You->" + msg, "tag_your_message")

    tkDisplay.config(state=tk.DISABLED)
    print(msg)

    send_mssage_to_server(msg, window)

    tkDisplay.see(tk.END)
    tkMessage.delete('1.0', tk.END)


def send_mssage_to_server(msg, window):
    content = {"ID": 3}
    msg = Message(content, "encode")
    sock.sendto(msg.toString().encode(), server)


def openChat():
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

    bottomFrame = tk.Frame(openChat)
    lblHeading = tk.Label(
        bottomFrame, text="Type the number of the chat you'd like to open:").pack(side=tk.TOP)

    chatNum = tk.Entry(bottomFrame)
    chatNum.pack(side=tk.BOTTOM)
    bottomFrame.pack(side=tk.TOP)


def openSpecificChat(chatID):
    content = {"ID": 9, "chatID": chatID}
    msg = Message(content, "encode")
    sock.sendto(msg.encode(), server)  # requests chat history

    pakcet, serverName = sock.recvfrom(2048)
    msg = Message(packet, "decode")

    chatHistory = []
    # data in format [('127.0.0', ['hello', 'how are you', ' sttsfd']), ('123232.123', ['afadsfa', 'asdfasf', 'adfas'])
    items = msg.getData().split("_")

    for item in items:
        parts = item.split(":")
        ip = parts[0]
        messages = parts[1].split(",")
        temp = (ip, messages)
        chatHistory.append(temp)


def exitApp():
    print("exit")


def connect(IP, entIP, btnConn, tkMessage):
    global ip, client
    if len(IP) < 1:
        tk.messagebox.showerror(
            title="ERROR!!!", message="You MUST enter the IP address of the person you wish to chat with <e.g. 203.0.113.42>")
    else:
        ip = IP
        entIP.config(state=tk.DISABLED)
        btnConn.config(state=tk.DISABLED)
        tkMessage.config(state=tk.NORMAL)
        ips = ip + " " + entIP
        content = {"ID": 2, "data": ips}
        msg = Message(content, "encode")
        sock.sendto(msg.toString().encode(), server)


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
