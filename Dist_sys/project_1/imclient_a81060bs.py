import time
import im
import sys
server = im.IMServerProxy('https://web.cs.manchester.ac.uk/a81060bs/comp28112_ex1/IMserver.php')


""" PROTOCOL

THERE CAN ONLY BE 1 MESSAGE IN THE SERVER.
IO: ONE KEY-VALUE PAIR
THE PROTOCOL FOLLOWS FIRST COME FIRST SERVE SCHEMA
SO IF YOU RUN THE PROGRAM FIRST YOU WILL ONLY BE ABLE TO SEND ONE MESSAGE.
THEN YOU WILL HAVE TO WAIT FOR THE PERSON TO REPLY TO YOU BEFORE SENDING ANOTHER MESSAGE.

"""


            
            
def waitForResponse():
    waitMessage = "Waiting for response..."
    print(waitMessage, end='\r', flush=True)
    

def fetchOrWaitForResponse():
    newMessage = server['sender']
    while newMessage == server['sender']:
            time.sleep(0.1)
            waitForResponse()
            continue
    print("\n********** new Message! ********** \n")
    print(server['sender'])
           

            


def leaveConversation():
    state = input('If you want to leave the conversation, type "exit" otherwise press enter: ')
    if state.lower() == 'exit':
        print("Goodbye!")
        server['sender'] = 'Other user left the conversation.'
        server.clear()  
        sys.exit()  # kill the program

   



def sendMessage(username):
    if username =='sender':
        message = input('Type your message: ')
        server[username] = message
        print("\n\n***********  Message sent!  *********** \n\n")
    else:
        print("error")

    
def getUsers():
    userList = server.keys()
    return userList
    
def start():
    global user1, user2 
    # DUE TO THE NATURE OF THE SERVER
    # len(getUsers()) == 1 MEANS THAT THE SERVER IS EMPTY AND THERE ARE NO USERS.
    if len(getUsers()) == 1:
        # INITIAL IDENTIFIERS
        user1 = 'sender'
        user2 ='reciever'
        # there are no userrs so you are a sender
        message = input("Enter your message: ")
        server[user1] = message
        # YOU HAVE SEND A MESSAGE NOW WAIT FOR THE REPLY
        user1 = 'reciever'
        fetchOrWaitForResponse()
        leaveConversation()
    if len(getUsers()) == 2:
        # there is 1 user waiting for a response
        # OUTPUT HIS MESSAGE
        print(server['sender'])
        # NOW YOU ARE A SENDER
        user2 = 'sender'
        sendMessage(user2)
        # YOU HAVE SEND A MESSAGE NOW, SO YOU ARE A RECIEVER
        user2 ='reciever'
        user1 = 'sender'
        fetchOrWaitForResponse()
        leaveConversation()
        conversation()
    # elif user1==user2:
    #     # ERROR -- DEADLOCK
    #     solveDeadlock()
    # else:
    #     print("error")
        
        
def conversation():
    global user1, user2 
    # print("You are now messaging each other.")     # uncomment this line to see when we come here
    while True:
        if user1 == 'sender':
            message = input("Enter your message: ")
            server[user1] = message
            user1 = 'reciever'
            user2 = 'sender'
            fetchOrWaitForResponse()
            leaveConversation()
        if user2 == 'sender':
            user2 = 'sender'
            sendMessage(user2)
            user2 ='reciever'
            user1 ='sender'
            fetchOrWaitForResponse()
            leaveConversation()
        else:
            # DEADLOCK
            print(user1)
            print(user2)
            print("error")
            break


def solveDeadlock():
    server.clear()
    print("sorry, there was an error. Please try again.")
    print("Send you message again.")
    start()
   
start()








