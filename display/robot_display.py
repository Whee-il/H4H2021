import time
import zmq
from graphlib import BedGraph
from graphlib import BedNode
from draw_graphics import Renderer
from rgbmatrix import graphics
import time




if __name__ == '__main__':

    # Set up Graph

    n0 = BedNode(-1, [5], "A1", (5,7), occupied=True)
    n1 = BedNode(-1, [6], "A2", (15,7), occupied=True)
    n2 = BedNode(-1, [7], "A3", (25, 7), occupied=True)
    n3 = BedNode(-1, [8], "A4", (35, 7), occupied=True)
    n4 = BedNode(-1, [9,11], "  ", (45, 7), occupied=False)

    n5 = BedNode(-1, [0,6], "  ", (5, 24), occupied=False)
    n6 = BedNode(-1, [1,5,7], "  ", (15, 24), occupied=False)
    n7 = BedNode(-1, [2,6,8], "  ", (25, 24), occupied=False)
    n8 = BedNode(-1, [3,7,9], "  ", (35, 24), occupied=False)
    n9 = BedNode(-1, [8,4,10], "  ", (45, 24), occupied=False)

    n10 = BedNode(-1, [9,11], "  ", (57, 24), occupied=False)
    n11 = BedNode(-1, [4,10], "  ", (57, 7), occupied=False)

    node_lst = [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11]
    
    floor = BedGraph()
    for n in node_lst:
        floor.add_node(n)
    floor.construct()
    floor.print_data()

    rend = Renderer()

    rend.process(floor)

    time.sleep(2)

    in_idx = 10
    out_idx = 11

    #Set up the socket
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://192.168.1.200:5555")  #!!!!!!!!!!!!!!!!!!!!!!!Replace IP with raspberry Pi IP

    #status is the current state of the robot. 
    status = "Idle"

    src_idx = 0

    while True:
        #  Wait for next request from client
        message = socket.recv_string()
        print(message)
        #Respond with current status
        if(message == "update"):
            socket.send_string(status)

        #Return
        elif((status=="Arrived") and (message == "Return")):
            socket.send_string("Return") #lets the flask server know that the bot has recieved the command and is moving
            time.sleep(1)   #time.sleep represents running the movement of the bot
            path = [in_idx,out_idx]
            rend.traverse(path, floor)
            path = floor.getPath(out_idx, src_idx, len(node_lst))
            rend.traverse(path, floor)
            status = "Idle" #when the bot is done moving, set the status to idle

        #Call
        elif(status=="Idle" and (message != "Return")):
            print(message) #I.e. "A2"
            socket.send_string("Recieved") #lets the flask server know that the bot has recieved the command and is moving
            time.sleep(1)   #time.sleep represents running the movement of the bot
            src_idx = floor.getIdxFromName(message)
            print(src_idx)
            path = floor.getPath(src_idx, in_idx, len(node_lst))
            rend.traverse(path, floor)
            
            status = "Arrived" #when the bot gets to the base, update the status to arrived
        
