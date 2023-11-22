import socket
import psutil
import threading
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
        msgFromUser = input("Type your message: ")
        msgFromUserArr = msgFromUser.split(' ',1)

        message =msgFromUserArr[1]
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
        while(block):
            continue
        messages = ["message " + str(i) for i in range(1, 11)]
        hexType=bytes.fromhex("02")
        for message in messages:
            for interface_name, addrs in interfaces.items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:  # We only want to broadcast on IPv4 interfaces
                        ip = addr.address.rsplit('.', 1)[0] + '.255'  # Calculate the broadcast IP for 
                        sock.sendto(Dest+Sender+PrevSender+hexType+message.encode(), (ip, port))

        #send deleting lineddd
        block=True
        hexType=bytes.fromhex("03")
        for interface_name, addrs in interfaces.items():
            for addr in addrs:
                if addr.family == socket.AF_INET:  # We only want to broadcast on IPv4 interfaces
                    ip = addr.address.rsplit('.', 1)[0] + '.255'  # Calculate the broadcast IP for 
                    message="delete"
                    sock.sendto(Dest+Sender+PrevSender+hexType+message.encode(), (ip, port))

def listener():
    sock.bind(("0.0.0.0", port))
    global block
    while True:
        data, addr = sock.recvfrom(65535)
        sender=data[2:4]
        dest=data[0:2]
        print(dest==bytes.fromhex(address))
        if (sender!=bytes.fromhex(address) and dest==bytes.fromhex(address)):
            Dest=data[2:4]
            originalSender=bytes.fromhex(address)
            PrevSender=bytes.fromhex("00 00")
            message="ack"
            msgType=data[6]
            print(data)

            if msgType== 0: 
                sock.sendto(Dest+originalSender+PrevSender+bytes.fromhex("02")+message.encode(), addr)
            if msgType== 1: 
                print(data)
            if msgType== 2: 
                if currentDest==str(Dest):
                    block=False
            
        


# Broadcast a message
if __name__ == "__main__":
    send_thread=threading.Thread(target=send)
    listener_thread=threading.Thread(target=listener)
    listener_thread.start()
    send_thread.start()