import socket
import sys
from threading import Timer
import time
import select



#----------------------------------------------------------------------
# This code needs to be initialized first in order to send/recieve
# data from the ROV. This code is to be booted on the surface computer.
#----------------------------------------------------------------------

# Create a TCP/IP socket
sock_p_t = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

myIP = "169.254.138.174" 

# Server Addresses
# Socket Bindings:
# Pressure and Temperature: 10030
server_address_p_t = (myIP, 10030)

print 'Pressure server starting up on %s port %s' % server_address_p_t
sock_p_t.bind(server_address_p_t)
max_time = 15.0

#Prevents socket being blocked by binding.
sock_p_t.setblocking(0)

try:
    while True:
        print '\nwaiting to receive message'
        did_timeout = True
        data_ready = select.select([sock_p_t], [], [], max_time)
        if data_ready[0]:
            data, address = sock_p_t.recvfrom(4096)
            print 'received %s bytes from %s' % (len(data), address)
            print data
            did_timeout = False

        if not did_timeout:
            if data:
                sent = sock_p_t.sendto(data, address)
                print 'sent %s bytes back to %s' % (sent, address)
            
        
except KeyboardInterrupt:
    print 'Does this work?'
    pass
finally:
    sock_p_t.close()
