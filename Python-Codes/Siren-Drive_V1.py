"""
UNH ROV 2015/16
Control Code - SIREN

Drive Code V1.0 by Shawn Swist
"""

# ================================================================
#      ----------     Necessary libraries   ------------
from Adafruit_PWM_Servo_Driver import PWM
from ControlFunctions import MotorControl, WriteMotor, Correction

import socket
import sys

from SendReceive import SendReceive

import time     # may not be necessary for final build

# ===================================================================
#    ----------------- Inatilization commands ----------------

# Define the hat over the I2C connection pins
hat = PWM(0x40)

# Set the desired frequency for the servos (50 Hz)
f = 48
hat.setPWMFreq(f)

# Define the thruster pins on the ServoHat
thruster1 = 0;
thruster2 = 2;
thruster3 = 4;
thruster4 = 6;
thruster5 = 8;
thruster6 = 10;
thruster7 = 12;
thruster8 = 14;

center = 307    # Use this to initilize the thrusters


# Add arduino and PC serial ports
arduino = serial.Serial('/dev/ttyACM0',115200) # 'serial port',baudrate
# PC UDP socket built into SendReceive


# Initilize
print "Initilizing ..."
hat.setPWM(thruster1, 0, center)
hat.setPWM(thruster2, 0, center)
hat.setPWM(thruster3, 0, center)
hat.setPWM(thruster4, 0, center)
hat.setPWM(thruster5, 0, center)
hat.setPWM(thruster6, 0, center)
hat.setPWM(thruster7, 0, center)
hat.setPWM(thruster8, 0, center)
# Initilize thrusters for 3 seconds
time.sleep(3)





while True:
    # Communication with PC

    # Read in game controller values
    LX,LY,RX,RY,LT,RT = SendReceive(message)

    MotorControl(RX,RY,LX,LY,RT,LT)

    print LX, LY, RX, RY, LT, RT

    #temp,pressure = ReadSensors()

    # Sital PID controller

    












