import socket
import psutil
import time
import threading

address="BB 04"
RoutingTable=[]
timer=0
def addToRoutingTable(originalSender,dest,addr):
    isThere=False
    for i in range(len(RoutingTable)):
        if(RoutingTable[i][0]==str(originalSender)and RoutingTable[i][1]==(str(dest))):
            isThere=True
            break
    if(not isThere):
        RoutingTable.append([str(originalSender),str(dest),addr,timer])
def listen_udp(port=50000):
    print("Listeing")
    """Listen for UDP broadcasts on a specific port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", port))
    while True:
        global RoutingTable
        global timer
        data, addr = sock.recvfrom(65535)
        dest=data[:2]
        originalSender=data[2:4]
        sender=data[4:6]
        msgType=data[6]
        message=data[7:]
        interfaces = psutil.net_if_addrs()
        senderip=addr[0]
        
        if (sender!=bytes.fromhex(address)):
            print(data)
            if(msgType==3):

                ipAddress=""
                for i in range(len(RoutingTable)):
                    if((RoutingTable[i][0]==str(dest) and RoutingTable[i][1]==str(originalSender))):
                        ipAddress=RoutingTable[i][2]
                        break
                tempTable=[]
                for i in range(len(RoutingTable)):       
                    if((RoutingTable[i][0]==str(originalSender) and RoutingTable[i][1]==str(dest)) or (RoutingTable[i][0]==str(dest) and RoutingTable[i][1]==str(originalSender))):
                        continue
                    else:
                        tempTable.append(RoutingTable[i])
                RoutingTable=tempTable
                hexMsgType=bytes.fromhex("03")
                try:
                    print(ipAddress)
                    sock.sendto(dest+originalSender+bytes.fromhex(address)+hexMsgType+message,ipAddress)
                except:
                    print("something went wrong")


            else:
                addToRoutingTable(originalSender, dest, addr)
                #routing table is not empty
                isSent=False
                for routes in RoutingTable:
                    if(routes[0]==str(dest)):
                        if(msgType==1):
                            hexMsgType=bytes.fromhex("01")
                        if(msgType==0):
                            hexMsgType=bytes.fromhex("00")
                        if(msgType==2):
                            hexMsgType=bytes.fromhex("02")
                        if(msgType==4):
                            hexMsgType=bytes.fromhex("04")
                        if(msgType==5):
                            hexMsgType=bytes.fromhex("05")
                        print("direct")
                        routes[3]=timer
                        sock.sendto(dest+originalSender+bytes.fromhex(address)+hexMsgType+message,routes[2])
                        isSent=True
                if(not isSent):
                        #add to list
                    if(msgType==1):
                        hexMsgType=bytes.fromhex("01")
                    if(msgType==0):
                        hexMsgType=bytes.fromhex("00")
                    if(msgType==2):
                        hexMsgType=bytes.fromhex("02")
                    if(msgType==4):
                        hexMsgType=bytes.fromhex("04")
                    if(msgType==5):
                        hexMsgType=bytes.fromhex("05")
                    for interface_name, addrs in interfaces.items():
                        for addr in addrs:
                            if addr.family == socket.AF_INET:  # We only want to broadcast on IPv4 interfaces
                                ip = addr.address.rsplit('.', 1)[0] + '.255'  # Calculate the broadcast IP for 
                                if senderip.startswith(addr.address.rsplit('.', 1)[0]):
                                    continue  # Skip this network
                                else:
                                    sock.sendto(dest+originalSender+bytes.fromhex(address)+hexMsgType+message, (ip, port))     
                    print("broadA")

def increase_counter():
    global RoutingTable
    global timer
    while True:
        timer += 1
        tempTable=[]
        for i in range(len(RoutingTable)):       
            if(timer-RoutingTable[i][3]>5):
                continue
            else:
                tempTable.append(RoutingTable[i])
        RoutingTable=tempTable
        time.sleep(1)

def askRoutingTable():
    global RoutingTable
    while(True):
        msgFromUser = input("Type your message: ")
        if msgFromUser=="table":
            print("table")
            print(RoutingTable)
# Listen for broadcasts
if __name__ == "__main__":
    askRoutingTable_thread=threading.Thread(target=askRoutingTable)
    timer_thread=threading.Thread(target=increase_counter)
    timer_thread.start()
    askRoutingTable_thread.start()
    listen_udp()

