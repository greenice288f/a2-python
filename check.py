import socket

# Get the list of all network interfaces
interfaces = psutil.net_if_addrs()
for interface_name, addrs in interfaces.items():
    for addr in addrs:
        if addr.family == socket.AF_INET:  # We only want to broadcast on IPv4 interfaces
            ip = addr.address.rsplit('.', 1)[0] + '.255'  # Calculate the broadcast IP for 
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            message = "Your message here"
            port = 50000  # Your port number here

            # Send the broadcast
            sock.sendto(message.encode(), (ip, port))
