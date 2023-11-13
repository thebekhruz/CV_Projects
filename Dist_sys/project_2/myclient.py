import sys
from ex2utils import Client

"""
***********
Running my code:
1. start the server using python3 myServer.py localhost 8080
2. connect to the server using python3 myClient.py localhost 8080
3. Register by providing a username
4. test the functionality of the client.
available commands:
Replace username with the username of the user you want to send a message to.
'@everyone' to send a message to all users.
'@username' to send a private message to a specific user. 
'@' to see a list of users currently connected to the chat.
'@block username' to block a user.
'@unblock username' to unblock a user.
'@quit' to leave the chatroom.
'@help' for a list of commands.



"""


class MyClient(Client):

	def onMessage(self, socket, message):
		# Print any message received from the server
		print(message)
		return True

	def sendMessage(self, message):
		# Send a message to the server
		self.send(message.encode())

# Parse the IP address and port you wish to connect to.
ip = sys.argv[1]
port = int(sys.argv[2])

# Create a client instance
client = MyClient()

# Start the client
client.start(ip, port)


flag = True
while flag:
	message = input("> ") 

	if message.lower() == "@quit":
		client.send(message.encode())
		flag = False
		break
	else:
		# Send message to the server
		print("Command sent to server!")
		client.send(message.encode())

		

client.stop()
