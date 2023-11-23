import socket
import psutil
import threading
import time

#broadcasting
bufferSize = 65535
address="AA 02"
RoutingTable=[]
port=50000
"""Broadcast a UDP message on a specific port."""
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
interfaces = psutil.net_if_addrs()
block = True
currentDest=""
timer=0
def inRoutingTable(dest):
    for routes in RoutingTable:
        if(routes[0]==str(dest)):
            return True
    return False
#0- searching,1 hi im here, message, 2 reply, 3 last one
def send():
    print("sender is up")

    while True:
        global currentDest
        global block
        global timer
        block =True
        msgFromUser = input("Type your message: ")
        msgFromUserArr = msgFromUser.split(' ',1)
        msgFromUser=msgFromUserArr[1]
        message ="searching"
        Dest = msgFromUserArr[0][:2] + " " + msgFromUserArr[0][2:]
        Dest = bytes.fromhex(Dest)
        currentDest=str(Dest)
        Sender=bytes.fromhex(address)
        PrevSender=bytes.fromhex("00 00")
        hexType=bytes.fromhex("00")

        #sending initial
        for interface_name, addrs in interfaces.items():
            for addr in addrs:
                if addr.family == socket.AF_INET:  # We only want to broadcast on IPv4 interfaces
                    ip = addr.address.rsplit('.', 1)[0] + '.255'  # Calculate the broadcast IP for 
                    sock.sendto(Dest+Sender+PrevSender+hexType+message.encode(), (ip, port))
        print("sent")
        initialTimer=timer
        quitByTimer=False
        while(block):
            if(timer-initialTimer>=5):
                block=False
                quitByTimer=True
            continue
        if(not quitByTimer):
            #messages = ["message " + str(i) for i in range(1, 11)]
            hexType=bytes.fromhex("02")
            #for message in messages:
            for interface_name, addrs in interfaces.items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:  # We only want to broadcast on IPv4 interfaces
                        ip = addr.address.rsplit('.', 1)[0] + '.255'  # Calculate the broadcast IP for 
                        sock.sendto(Dest+Sender+PrevSender+hexType+msgFromUser.encode(), (ip, port))

            #send deleting lineddd
            block=True
            hexType=bytes.fromhex("03")
            for interface_name, addrs in interfaces.items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:  # We only want to broadcast on IPv4 interfaces
                        ip = addr.address.rsplit('.', 1)[0] + '.255'  # Calculate the broadcast IP for 
                        message="delete"
                        sock.sendto(Dest+Sender+PrevSender+hexType+message.encode(), (ip, port))
        else:
            print("time out")

def listener():
    sock.bind(("0.0.0.0", port))
    global block
    while True:
        data, addr = sock.recvfrom(65535)
        sender=data[2:4]
        dest=data[0:2]
        if (sender!=bytes.fromhex(address) and dest==bytes.fromhex(address)):
            Dest=data[2:4]
            originalSender=bytes.fromhex(address)
            PrevSender=bytes.fromhex("00 00")
            message="ack"
            msgType=data[6]
            if msgType== 0: 
                sock.sendto(Dest+originalSender+PrevSender+bytes.fromhex("01")+message.encode(), addr)
            if msgType== 1: 
                if currentDest==str(Dest):
                    block=False
            if msgType== 2: 
                print(data)

            
def increase_counter():
    global timer
    while True:
        timer += 1
        time.sleep(1)



# Broadcast a message
if __name__ == "__main__":
    send_thread=threading.Thread(target=send)
    listener_thread=threading.Thread(target=listener)
    timer_thread=threading.Thread(target=increase_counter)
    timer_thread.start()
    listener_thread.start()
    send_thread.start()