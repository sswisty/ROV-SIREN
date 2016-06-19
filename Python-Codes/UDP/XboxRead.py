import pygame
from pygame.locals import *
import os, sys
import threading
import time

from XboxControllerReadValues import *

XboxCont = XboxController( deadzone = 10, scale = 40, invertYAxis = True)


try:
    xboxCont.start()
    while True:
        Lx, Ly, Rx, Ry, Lt, Rt, dpad = GetValues()

        PadUD = dpad[1]
        PadLR = dpad[0]

       
        print Lx, Ly, Rx, Ry, Lt, Rt, PadUD, PadLR
        
        
except KeyboardInterrupt:
    print "User Cancelled"

except:
    print "unexpected error"

finally:
    xboxCont.stop()
