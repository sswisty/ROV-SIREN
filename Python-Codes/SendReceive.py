import socket
import sys

def SendReceive(message1, message2):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_ip = "169.254.138.174"
    server_address = (server_ip, 10030)

    try:
        # Send Data
        print 'sending "%s"' % message
        sent = sock.sendto(message1, server_address)
        sent = sock.sendto(message2, server_address)

        # Receive Response
        Lx, server = sock.recvfrom(4096)
        Ly, server = sock.recvfrom(4096)
        Rx, server = sock.recvfrom(4096)
        Ry, server = sock.recvfrom(4096)
        Lt, server = sock.recvfrom(4096)
        Rt, server = sock.recvfrom(4096)
        PadUD, server = sock.recvfrom(4096)
        PadLR, server = sock.recvfrom(4096)

        #print 'Recieved', Lx, Ly, Rx, Ry, Lt, Rt

        sock.close() # Closes socket

        Lx = int(float(Lx))
        Ly = int(float(Ly))
        Rx = int(float(Rx))
        Ry = int(float(Ry))
        Lt = int(float(Lt))
        Rt = int(float(Rt))
        PadUD = int(float(PadUD))
        PadLR = int(float(PadLR))

        return Lx, Ly, Rx, Ry, Lt, Rt, PadUD, PadLR

    finally:
        sock.close()

        
