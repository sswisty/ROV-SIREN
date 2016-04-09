import socket
import sys

#----------------------------------------------------------------------------
# This code need to be initalized second in order to send/recieve data from
# the computer. This code should be initalized when the ROV turns on.
#----------------------------------------------------------------------------

from SendRecieve import SendRecieve

# Message to be sent to surface computer
message_p_t= raw_input("Pressure/Temperature reading: ")

# Running counter
counter  = 1
while True:
    SendRecieve(message_p_t)
    print counter
    counter += 1
