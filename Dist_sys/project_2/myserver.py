"""

Network server skeleton.

This shows how you can create a server that listens on a given network socket, dealing
with incoming messages as and when they arrive. To start the server simply call its
start() method passing the IP address on which to listen (most likely 127.0.0.1) and 
the TCP port number (greater than 1024). The Server class should be subclassed here, 
implementing some or all of the following five events. 

  onStart(self)
      This is called when the server starts - i.e. shortly after the start() method is
      executed. Any server-wide variables should be created here.
      
  onStop(self)
      This is called just before the server stops, allowing you to clean up any server-
      wide variables you may still have set.
      
  onConnect(self, socket)
      This is called when a client starts a new connection with the server, with that
      connection's socket being provided as a parameter. You may store connection-
      specific variables directly in this socket object. You can do this as follows:
          socket.myNewVariableName = myNewVariableValue      
      e.g. to remember the time a specific connection was made you can store it thus:
          socket.connectionTime = time.time()
      Such connection-specific variables are then available in the following two
      events.

  onMessage(self, socket, message)
      This is called when a client sends a new-line delimited message to the server.
      The message paramater DOES NOT include the new-line character.

  onDisconnect(self, socket)
      This is called when a client's connection is terminated. As with onConnect(),
      the connection's socket is provided as a parameter. This is called regardless of
      who closed the connection.

"""


""" TODO:
 * update your functionality list
 * when blocking the user add more checking functionality. 
 """

import sys
from ex2utils import Server

class MyServer(Server):


    def onStart(self):
        # Task 2.2 
        self.numberOfConnections = 0
        # I want to store all usernames in a lowercase dictionary
        self.usernameDictionary = {}
        self.IdDictionary = {}
        # Blocked: bywho?
        self.blockedUsers = {}
        print ("Server started.")
    
    def onStop(self):
        print ("Server stopped.")

    def onConnect(self, socket):
        self.numberOfConnections +=1
        print ("Client connected.")
        print ("Number of clients: " + str(self.numberOfConnections))
        socket.username = ''
        socket.send("You must register before you can send messages.\n  Enter you username: ".encode())
    
    def onMessage(self, socket, message):
        # all users must be registered before they can send messages
        username = socket.username
        

        # Check if username is registered
        if socket.username == '':
            rawMessage = message.strip().partition(' ')
            username = rawMessage[0]
            # All usernames must be lowercase
            username = username.lower()
            self.registerUser(socket, username)
            return True
        

        # If username is regisitered allow him to send commands/messages
        elif username != '':
            """ ********************* Task 2.3 *************************** """

            rawMessage = message.strip().partition(' ')
            # The command is the first word
            command = rawMessage[0]
            print ("Command is :: " + ''.join(command))
            # Parameters are the rest of the message
            parameters = rawMessage[2:]
            print ("Parameters are :: " + ''.join(parameters))

            message = message.encode()
            print ("Message received: %s" % message.decode())
            """ ************************************************ """




            command = command.lower() # convert to lower case for case-insensitive matching
            # Send message to all connected users
            if command == "@everyone":
                # Check how many users are connected
                if self.numberOfConnections == 1:
                    socket.send("Error: no users connected.\n".encode())
                    return True
                else:
                    for reciever in self.usernameDictionary.values():
                        # Do not send message to yourself
                        if reciever.username == socket.username:
                            # signify that the message was sent to everyone
                            # reciever.send("Message has been sent!".encode())
                            continue
                        else:
                            # Transform tuple to string
                            parameters = ' '.join(rawMessage[2:]).strip()
                            
                            # Send message
                            reciever.send(f"{socket.username} says: {parameters}\n".encode())
                            return True

            # Print the list of connected users
            elif command == '@':
                connectedUsers = ', '.join(self.usernameDictionary)
                socket.send(f"Connected users: {connectedUsers}\n".encode())
                return True
            

            # Command to close connection:
            elif command == '@quit':
                socket.send("Goodbye!\n".encode())
                del self.usernameDictionary[socket.username]
                # when you call onDisconnect it will be called twice so you need to add number of connections +1
                self.numberOfConnections += 1
                # self.onStop()
                # Close
                self.onDisconnect(socket)
                return False
            
            # Lets allow users to block unwanted users
            elif command == '@block':
                blockThisUser = parameters[0]
                # check if the user has provided username as argument
                if blockThisUser == '':
                    socket.send("You must provide a username.\n".encode())
                    return True
                # check that the username exsists
                elif blockThisUser not in self.usernameDictionary:
                    socket.send("Error: user does not exist.\n".encode())
                    return True
                elif blockThisUser == socket.username:
                    socket.send("Error: you can't block yourself.\n".encode())
                    return True
                
                elif blockThisUser in self.blockedUsers:
                    socket.send(blockThisUser.encode())
                    socket.send(parameters[0].encode())
                    socket.send("Error: user is already blocked\n".encode())
                    return True
                else:
                    blockthisuser = "".join(parameters)
                    self.blockedUsers[blockthisuser] = socket.username
                    socket.send("User is now blocked\n".encode())
                    return True

            # Command to unblock a user
            elif command == '@unblock':
                unblockThisUser = parameters[0].lower()
                # Check if user is blocked
                if unblockThisUser in self.blockedUsers and self.blockedUsers[unblockThisUser] == socket.username:
                    del self.blockedUsers[unblockThisUser]
                    print(self.blockedUsers)
                    socket.send(f"{unblockThisUser} has been unblocked.\n".encode())
                    return True
                else:
                    socket.send("Error: user is not blocked by you.\n".encode())
                return True

            elif command == '@help':
                socket.send(
        """Commands:
Replace username with the username of the user you want to send a message to.
- Type '@everyone' to send a message to all users.
- Type '@username' to send a private message to a specific user. 
- Type '@' to see a list of users currently connected to the chat.
- Type '@block username' to block a user.
- Type '@unblock username' to unblock a user.
- Type '@quit' to leave the chatroom.
- Type '@help' for a list of commands.

 """.encode())
                return True


            # Send a message to a specific user
            elif (command.startswith("@")):
                # get the recipient's username
                reciever = command[1:].lower()
                # check if you have blocked this user
                if reciever in self.blockedUsers and self.blockedUsers[reciever] == socket.username:
                    socket.send(f"You have blocked {reciever}. Message can't be delivered\n".encode())
                    return True
                # check if the user has blocked you
                elif socket.username in self.blockedUsers and self.blockedUsers[socket.username] == reciever:
                    socket.send(f" {reciever} has blocked you. Message can't be delivered.\n".encode())
                    return True
                else:
                    if reciever in self.usernameDictionary:
                        print(username)
                        recieverSocket = self.usernameDictionary[reciever]
                        parameters = ' '.join(rawMessage[2:]).strip()
                        recieverSocket.send(f"{socket.username} says: {parameters}\n".encode())
                        return True
                    else:
                        socket.send("Error: user not found\n Try again.".encode())
                        return True


            else:
                # Send error message to user
                socket.send("Error: invalid command\n".encode())
                return True

        # Unexpected Errors
        else:
           socket.send("Error: Unexpected Error\n".encode())
           return True
        
   
        # return True



    def onDisconnect(self, socket):
        self.numberOfConnections -= 1
        print ("Client disconnected.")
        print ("Number of clients: " + str(self.numberOfConnections))
        return False
        # Delete data about user
        # del self.usernameDictionary[socket.username]


    def registerUser(self, socket, username):
        while True:
            if len(username) > 16:
                socket.send("Error: username is too long\n Try again: ".encode())
                socket.username = ''
                return
            elif len(username) < 3:
                socket.send("Error: username is too short\n Try again: ".encode())
                socket.username = ''
                return
            elif username in self.usernameDictionary:
                socket.send("Error: username is already in use\n Try again: ".encode())
                socket.username = ''
                return
            elif not all(char.isalnum() for char in username):
                socket.send("Error: username can only contain alphabetic and numeric characters\n Try again: ".encode())
                socket.username = ''
                return
            else:
                
                socket.username = username
                self.usernameDictionary[socket.username] = socket
                socket.send(f"Welcome {socket.username}!\n".encode())
                socket.send(
        """Welcome to the chatroom! Here are some commands you can use:
Replace username with the username of the user you want to send a message to.
- Type '@everyone' to send a message to all users.
- Type '@username' to send a private message to a specific user. 
- Type '@' to see a list of users currently connected to the chat.
- Type '@block username' to block a user.
- Type '@unblock username' to unblock a user.
- Type '@quit' to leave the chatroom.
- Type '@help' for a list of commands.
 """.encode())
                return True
        

    def blockUser(self, socket, username):
        # Check if username is provided as argument
        if username is None:
            # If not, notify the user and return
            socket.send("Please provide a username to block.\n".encode())
            return True

        # Check if the username exists
        if username.lower() not in self.usernameDictionary:
            # If not, notify the user and return
            socket.send(f"Username {username} is not found.\n".encode())
            return True

        # Check if the user is already blocked
        if username.lower() in socket.blocked_users:
            # If so, notify the user and return
            socket.send(f"You have already blocked {username}.\n".encode())
            return True

        # Block the user and notify the user
        socket.blocked_users.append(username.lower())
        socket.send(f"You have blocked {username}.\n".encode())
        return True


    





# Parse the IP address and port you wish to listen on.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create an echo server.
server = MyServer()

# If you want to be an egomaniac, comment out the above command, and uncomment the
# one below...
#server = EgoServer()

# Start server
server.start(ip, port)

