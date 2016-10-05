# UNH ROV SIREN DRIVE STATION CODE FOR MATE 2016
# NASA NEUTURAL BUOYANCY LAB - HOUSTON, TX


# =================================================================
# Necessary Libraries (?)

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


# ==================================================================
# UDP Socket (client...)



def SendStuff(data1,data2,data3,data4,data5,data6,data7,data8,data9):

    ROV_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    IP = "169.254.58.111"
    port = 10070

    server_address = (IP,port)

    #data = str(314)


    try:
        # Send Data
        print 'Sending Controller Values'
        sent_1 = ROV_socket.sendto(data1, server_address)
        sent_2 = ROV_socket.sendto(data2, server_address)
        sent_3 = ROV_socket.sendto(data3, server_address)
        sent_4 = ROV_socket.sendto(data4, server_address)
        sent_5 = ROV_socket.sendto(data5, server_address)
        sent_6 = ROV_socket.sendto(data6, server_address)
        sent_7 = ROV_socket.sendto(data7, server_address)
        sent_8 = ROV_socket.sendto(data8, server_address)
        data_9 = ROV_socket.sendto(data9, server_address)
        #print 'Sent "%s" to Siren' % data

        #print 'Attempting to recieve data'
        incoming, in_server = ROV_socket.recvfrom(4096)
        #print 'Recievved "%s" from Siren' % incoming
        print incoming

        ROV_socket.close()

    except KeyboardInterrupt:
        print 'User Cancled.'

    finally:
        print 'Closing socket'
        ROV_socket.close()

# =============================================
# Actual comms loop

try:
    xboxCont.start()
    while True:
        LX, LY, RX, RY, LT, RT, DPAD, A = GetValues()
        LX = round(LX)
        LY = round(LY)
        RX = round(RX)
        RY = round(RY)
        LT = round(LT)
        RT = round(RT)
        
        DpadUD = DPAD[1]
        DpadLR = DPAD[0]
        data = 'LX: %s | LY: %s | RX: %s | RY: %s | LT: %s | RT: %s | DpadUD: %s | DpadLR: %s' %(LX, LY, RX, RY, LT, RT, DpadUD, DpadLR)
        data = '%s %s %s %s %s %s %s %s' %(LX, LY, RX, RY, LT, RT, DpadUD, DpadLR)
        #print 'Controller Reading: %s' % data
        SendStuff(str(LX),str(LY),str(RX),str(RY),str(LT),str(RT),str(DpadUD),str(DpadLR),str(A))
except KeyboardInterrupt:
    print "User Cancled"

finally:
    xboxCont.stop()
    
