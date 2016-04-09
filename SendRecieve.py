import socket
import sys

def SendRecieve(message_p_t):

    sock_p_t = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_ip = "169.254.138.174"
    server_address = (server_ip, 10030)
    

    try: 
        # Send data
        print 'sending "%s"' % message_p_t
        sent_p_t = sock_p_t.sendto(message_p_t, server_address)

        # Receive response
        print 'waiting to receive'
        data, server = sock_p_t.recvfrom(4096)
        print 'received "%s"' % data

        sock_p_t.close() #Closes socket

    finally:
        print 'closing socket'
        sock_p_t.close() #Ensures that the socket closes upon completion
