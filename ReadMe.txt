This servers as a guide for using the chat application code attached


Python 3 should be installed as well as tkinter.
This package comes pre-installed with python but we have found that in some cases it may be missing.
To install it on Linux run:
sudo apt-get install python3-tk

To begin open the Server.py and Client.py classes.
Enter the IP address of the computer that will run the server into the host field on line 10 of Server.
Enter the same IP adress on every instance of the client class in the variable ServerName on line 11 of Client.py

Once the IP adderess of the Server and Client are setup run the Server.py class.
You should see ready to recieve ... printed out.
To end the server class at any point type "exit" and press enter

Note: If you are running the server class on a windows computer.
There is a portion of code that cannot run on windows computers but works on Mac and Linux.
If you wish to run on windows comment out lines 146 to 149 in Server.py. The lines tarting with i,o,e and the entire if statement.
When you run server it will no longer exit when you type "exit" you have to manually end the program

Now run the Client.py. Conected should be printed out to the terminal.
On the sever side it should print "Connected to client with IP: xxx.xxx.xxx.xxx on port: xxxx"
From the on the Client.py program may be ended by clicking on the exit button on the GUI. 

Note: If you do not end the server instance correctly and attempt to run it again you may recieve an error because the socket is already in use.
To fix this change the port number on the server and client sides and run again. 

