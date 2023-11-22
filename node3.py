import socket
import psutil

address="BB 03"
def listen_udp(port=50000):
    """Listen for UDP broadcasts on a specific port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.bind(("0.0.0.0", port))
    RoutingTable=[]
    while True:
        data, addr = sock.recvfrom(65535)
        dest=data[:2]
        sender=data[2:4]
        prevSender=data[4:6]
        msgType=data[6]
        message=data[7:]
        interfaces = psutil.net_if_addrs()
        senderip=addr[0]
        if (sender!=bytes.fromhex(address) and prevSender!=bytes.fromhex(address)):
            print(data)
            if not RoutingTable: #check if the list is empty
                RoutingTable.append([str(sender),addr])
                if(msgType==1):
                    hexMsgType=bytes.fromhex("01")
                else:
                    hexMsgType=bytes.fromhex("00")
                for interface_name, addrs in interfaces.items():
                    for addr in addrs:
                        if addr.family == socket.AF_INET:  # We only want to broadcast on IPv4 interfaces
                            ip = addr.address.rsplit('.', 1)[0] + '.255'  # Calculate the broadcast IP for 
                            if senderip.startswith(addr.address.rsplit('.', 1)[0]):
                                print(f"Skipping sender's network: {ip}")
                                continue  # Skip this network
                            else:
                                sock.sendto(dest+bytes.fromhex(address)+sender+hexMsgType+message, (ip, port))
            else:
                isSent=False
                for routes in RoutingTable:
                    if(routes[0]==str(dest)):
                        #send it specific address
                        if(msgType==1):
                            hexMsgType=bytes.fromhex("01")
                        else:
                            hexMsgType=bytes.fromhex("00")
                        sock.sendto(dest+bytes.fromhex(address)+sender+hexMsgType+message,routes[1])
                        isSent=True
                if(not isSent):
                        #add to list
                        if(msgType==1):
                            hexMsgType=bytes.fromhex("01")
                        else:
                            hexMsgType=bytes.fromhex("00")
                        RoutingTable.append([str(sender),addr])
                        for interface_name, addrs in interfaces.items():
                            for addr in addrs:
                                if addr.family == socket.AF_INET:  # We only want to broadcast on IPv4 interfaces
                                    ip = addr.address.rsplit('.', 1)[0] + '.255'  # Calculate the broadcast IP for 
                                    if senderip.startswith(addr.address.rsplit('.', 1)[0]):
                                        print(f"Skipping sender's network: {ip}")
                                        continue  # Skip this network
                                    else:
                                        sock.sendto(dest+bytes.fromhex(address)+sender+hexMsgType+message, (ip, port))            

# Listen for broadcasts
if __name__ == "__main__":
    listen_udp()
