# Siren PC Drive Station DEBUG PROGRAM

# IMPORT
import socket
import sys
from threading import Timer
import time
import select
from random import *
import pygame
from pygame.locals import *
import os, sys
from XboxControllerReadValues import *


# XBOX CONTROLLER
XboxCont = XboxController( deadzone = 10, scale = 50, invertYAxis = True)
print 'Controller Established \n'


# Create a TCP/IP socket
sock_p_t = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
myIP = "169.254.202.234"   # CHANGE THIS IF NECESSARY

server_address_p_t = (myIP, 10030) # make sure we have the right port...

print 'Server Established /n'


sock_p_t.bind(server_address_p_t)
print 'Socket Binded /n'

max_time = 15.0

#Prevents socket being blocked by binding.
sock_p_t.setblocking(0)
print 'socket blocking (?) not sure what this does /n'



print 'Starting Communications with Pi  on %s port %s' % server_address_p_t



try:
    xboxCont.start()
    while True:

        Lx, Ly, Rx, Ry, Lt, Rt, dpad = GetValues()
        PadUD = dpad[1]
        PadLR = dpad[0]
        print "LX INPUT TO ROV:", Lx
        
        print '\nwaiting to receive message'
        did_timeout = True
        data_ready = select.select([sock_p_t], [], [], max_time)
        if data_ready[0]:
            in_pressure, address = sock_p_t.recvfrom(4096)
            in_temp, address = sock_p_t.recvfrom(4096)
            print 'received %s bytes from %s' % (len(in_pressure), address)
            print in_pressure
            did_timeout = False

        if not did_timeout:
            if data:

                # these represent the axis valeus...
                Lx = round(Lx)
                Ly = round(Ly)
                Rx = round(Rx)
                Ry = round(Ry)
                Lt = round(Lt)
                Rt = round(Rt)
                PadUD = round(PadUD)
                PadLR = round(PadLR)

                Lx = str(Lx)
                Ly = str(Ly)
                Rx = str(Rx)
                Ry = str(Ry)
                Lt = str(Lt)
                Rt = str(Rt)
                PadUD = str(PadUD)
                PadLR = str(PadLR)
                
                print "SENDING!"
                sent1 = sock_p_t.sendto(Lx, address)
                sent2 = sock_p_t.sendto(Ly, address)
                sent3 = sock_p_t.sendto(Rx, address)
                sent4 = sock_p_t.sendto(Ry, address)
                sent5 = sock_p_t.sendto(Lt, address)
                sent6 = sock_p_t.sendto(Rt, address)
                sent7 = sock_p_t.sendto(PadUD, address)
                sent8 = sock_p_t.sendto(PadUD, address)
                print 'sent %s bytes back to %s' % (sent1, address)
       
                print Lx, Ly, Rx, Ry, Lt, Rt
        
        
except KeyboardInterrupt:
    print "User Cancelled"

except:
    print "unexpected error"

finally:
    xboxCont.stop()
    sock_p_t.close()































