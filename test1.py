import socket
import psutil

address="BB 01"
def listen_udp(port=50000):
    """Listen for UDP broadcasts on a specific port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    RoutingTable=[]

    interfaces = psutil.net_if_addrs()

    print(socket.AF_INET)
    for interface_name, addrs in interfaces.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:  # We only want to broadcast on IPv4 interfaces
                print(addr)
                ip = addr.address.rsplit('.', 1)[0] + '.255'  # Calculate the broadcast IP for 
                print(ip)

# Listen for broadcasts
if __name__ == "__main__":
    listen_udp()
