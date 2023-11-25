import socket
import psutil
import threading
import time
import zlib
#broadcasting
bufferSize = 65535
address="AA 03"
RoutingTable=[]
port=50000
"""Broadcast a UDP message on a specific port."""
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
interfaces = psutil.net_if_addrs()
block = True
currentDest=""
timer=0
arrived=False
retry=True
currentRoute=""
def checksum_calculator(data):
    checksum = zlib.crc32(data)
    checksum = checksum%255
    return checksum

def checksumCalculatorB(data):
    checksum = zlib.crc32(data)
    checksum = checksum%255
    checksumb= checksum.to_bytes(1,"big")
    return checksumb
def inRoutingTable(dest):
    for routes in RoutingTable:
        if(routes[0]==str(dest)):
            return True
    return False
#0- searching,1 hi im here, message, 2 reply, 3 last one
def send():
    print("sender is up")

    while True:
        global arrived
        global currentDest
        global block
        global timer
        global retry
        block =True
        currentDest=""
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
        initialTimer=timer
        quitByTimer=False
        while(block):
            if(timer-initialTimer>=5):
                block=False
                quitByTimer=True
            continue
        if(not quitByTimer):
            retry=True
            
            hexType=bytes.fromhex("02") 
            checkSum=checksumCalculatorB(msgFromUser.encode())
            sock.sendto(Dest+Sender+PrevSender+hexType+checkSum+msgFromUser.encode(), currentDest)
            block=True
            initialTimer=timer
            quitByTimer=False

            while(block):
                if(timer-initialTimer>=5):
                    block=False
                    quitByTimer=True
                continue
            
            if(quitByTimer):
                block=True
                if(retry):
                    hexType=bytes.fromhex("02") 
                    checkSum=checksumCalculatorB(msgFromUser.encode())
                    sock.sendto(Dest+Sender+PrevSender+hexType+checkSum+msgFromUser.encode(), currentDest)
                    block=True
                    initialTimer=timer
                    quitByTimer=False

                    while(block):
                        if(timer-initialTimer>=5):
                            block=False
                            quitByTimer=True
                        continue

            #send deleting lineddd
            hexType=bytes.fromhex("03")
            message="delete"
            sock.sendto(Dest+Sender+PrevSender+hexType+message.encode(), currentDest)
        
        else:
            print("time out")

def listener():
    sock.bind(("0.0.0.0", port))
    global block
    global arrived
    global currentDest
    global retry
    while True:
        data, addr = sock.recvfrom(65535)
        sender=data[2:4]
        dest=data[0:2]
        if (sender!=bytes.fromhex(address) and dest==bytes.fromhex(address)):
            Dest=data[2:4]
            originalSender=bytes.fromhex(address)
            PrevSender=bytes.fromhex("00 00")
            messageA="ack"

            msgType=data[6]
            if msgType== 0: 
                sock.sendto(Dest+originalSender+PrevSender+bytes.fromhex("01")+messageA.encode(), addr)
            if msgType== 1: 
                if currentDest==str(Dest):
                    currentDest=addr
                    print("Route found")
                    block=False

            if msgType== 2: 
                messageFromEP=data[8:]
                checkSumFromPacket=data[7]
                checksum=checksum_calculator(messageFromEP)
                if(checkSumFromPacket==checksum):
                    print(data)
                    sock.sendto(Dest+originalSender+PrevSender+bytes.fromhex("04")+messageA.encode(), addr)
                else:
                    sock.sendto(Dest+originalSender+PrevSender+bytes.fromhex("05")+messageA.encode(), addr)
            if msgType== 4:
                print("ack Arrived") 
                block=False
                retry=False
            if msgType== 5:
                print("ack Arrived") 
                block=False
                retry=True


            
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