import sys
import socket
import constants as const


def main(argv):
    data       = "Hello UDP Server".encode()
    bufferSize = 65535

    # Use the first argument as name of the server to contact
    # omitted all checks and safety here
    addr = (argv[0], const.SERVER_PORT)

    # Create a UDP socket at client side
    socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Send to server using created UDP socket
    socket.sendto(data, addr)

    data, addr = socket.recvfrom(bufferSize)
    print("From:", addr, ":", data)

if __name__ == "__main__":
    main(sys.argv[1:])