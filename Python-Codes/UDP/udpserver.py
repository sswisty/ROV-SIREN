import socket
import sys
from threading import Timer
import time
import select
from random import *


#----------------------------------------------------------------------
# This code needs to be initialized first in order to send/recieve
# data from the ROV. This code is to be booted on the surface computer.
#----------------------------------------------------------------------

# Create a TCP/IP socket
sock_p_t = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

myIP = "169.254.202.234" 

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

                # these represent the axis valeus...
                new_data_1 = randint(0,10)
                new_data_2 = randint(0,10)
                new_data_3 = randint(0,10)
                new_data_4 = randint(0,10)
                new_data_5 = randint(0,10)
                new_data_6 = randint(0,10)
                new_data_1 = str(new_data_1)
                new_data_2 = str(new_data_2)
                new_data_3 = str(new_data_3)
                new_data_4 = str(new_data_4)
                new_data_5 = str(new_data_5)
                new_data_6 = str(new_data_6)

                sent1 = sock_p_t.sendto(new_data_1, address)
                sent2 = sock_p_t.sendto(new_data_2, address)
                sent3 = sock_p_t.sendto(new_data_3, address)
                sent4 = sock_p_t.sendto(new_data_4, address)
                sent5 = sock_p_t.sendto(new_data_5, address)
                sent6 = sock_p_t.sendto(new_data_6, address)
                print 'sent %s bytes back to %s' % (sent1, address)
            
        
except KeyboardInterrupt:
    print 'Does this work?'
    pass
finally:
    sock_p_t.close()
