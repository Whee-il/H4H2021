
import time
import zmq

#Set up the socket
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://192.168.1.200:5555")  #!!!!!!!!!!!!!!!!!!!!!!!Replace IP with raspberry Pi IP

#status is the current state of the robot. 
status = "Idle"
while True:
    #  Wait for next request from client
    message = socket.recv_string()
    
    #Respond with current status
    if(message == "update"):
        socket.send_string(status)

    #Return
    elif((status=="Arrived") and (message == "Return")):
        socket.send_string("Return") #lets the flask server know that the bot has recieved the command and is moving
        time.sleep(2)   #time.sleep represents running the movement of the bot
        status = "Idle" #when the bot is done moving, set the status to idle

    #Call
    elif(status=="Idle" and (message != "Return")):
        print(message) #I.e. "A2"
        socket.send_string("Recieved") #lets the flask server know that the bot has recieved the command and is moving
        time.sleep(2)   #time.sleep represents running the movement of the bot
        status = "Arrived" #when the bot gets to the base, update the status to arrived
    
