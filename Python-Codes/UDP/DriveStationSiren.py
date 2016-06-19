# ROV-SIREN Drive Code
'''
This code is to be run by the computer operating Siren.
Code uses pygame to read in xbox controller and UDP to send/receive data
from the Rasbperry Pi on Siren, running Siren-Drive_V1.py

Code by:
    Shawn Swist, Sital Khatiwada, Fritz Wallace

'''

# =======================================================
# ------------- NECESSARY LIBRARIES ---------------------
# =======================================================
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


# =======================================================
# ------------- SET UP COMMUNICATION --------------------
# =======================================================
# Create a TCP/IP socket
sock_p_t = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

myIP = "169.254.202.234"
# Must be IP address of the computer IPV4 ethernet connection

server_address_p_t = (myIP, 10030)

sock_p_t.bind(server_address_p_t)
max_time = 15.0

#Prevents socket being blocked by binding.
sock_p_t.setblocking(0)

print 'Rasbperry Pi Communications starting up on %s port %s' % server_address_p_t


# =======================================================
# ------------------- MAIN LOOP -------------------------
# =======================================================
XboxCont = XboxController( deadzone = 10, scale = 60, invertYAxis = True)

try:
    xboxCont.start()
    while True:

        # Read axis values from controller
        Lx, Ly, Rx, Ry, Lt, Rt, PadUD, PadLR = GetValues()
        
        print '\n    Waiting to receive message..'
        print '\n'
        did_timeout = True
        data_ready = select.select([sock_p_t], [], [], max_time)
        if data_ready[0]:
            data1, address = sock_p_t.recvfrom(4096)
            data2, address = sock_p_t.recvfrom(4096)
            #print 'received %s bytes from %s' % (len(data), address)
            print '\nROV CURRENT DEPTH: \t', data1
            print '\nROV CURRENT TEMP: \t', data2
            did_timeout = False
            print '\n'

        if not did_timeout:
            if data:
                # Round and turn controller values into strings
                Lx = round(Lx)
                Ly = round(Ly)
                Rx = round(Rx)
                Ry = round(Ry)
                Lt = round(Lt)
                Rt = round(Rt)
                
                Lx = str(Lx)
                Ly = str(Ly)
                Rx = str(Rx)
                Ry = str(Ry)
                Lt = str(Lt)
                Rt = str(Rt)
                PadUD = str(PadUD)
                PadLR = str(PadLR)
                
                print "\n       Sending values to Siren"
                sent1 = sock_p_t.sendto(Lx, address)
                sent2 = sock_p_t.sendto(Ly, address)
                sent3 = sock_p_t.sendto(Rx, address)
                sent4 = sock_p_t.sendto(Ry, address)
                sent5 = sock_p_t.sendto(Lt, address)
                sent6 = sock_p_t.sendto(Rt, address)
                sent7 = sock_p_t.sendto(PadUD, address)
                sent8 = sock_p_t.sendto(PadLR, address)
                #print 'sent %s bytes back to %s' % (sent1, address)
       
                print '\nInputs: \tLX \tLY \tRX \tRY \tLT \tRT'
                print '\t\t',Lx, '\t',Ly, '\t',Rx, '\t',Ry, '\t',Lt, '\t',Rt

        # Clear terminal window for optimal viewing experience
        print '\n\n\n\n\n\n\n\n\n\n\n\n'
        
except KeyboardInterrupt:
    print "User Cancelled"

except:
    print "unexpected error"

finally:
    xboxCont.stop()
    sock_p_t.close()







