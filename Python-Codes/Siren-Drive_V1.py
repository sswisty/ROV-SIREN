# UNH ROV 2015/16
# Control Code - SIREN




# =================================================================

# Necessary libraries
from Adafruit_PWM_Servo_Driver import PWM
from ControlFunctions import MotorControl

import time     # may not be necessary for final build

# Define the hat over the I2C connection pins
hat = PWM(0x40)

# Set the desired frequency for the servos (400 Hz)
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
PC = ... # not sure how to do this yet


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





while (Connection_Established):
    # Communication with PC

    # Read in game controller values
    RX,RY,LX,LY,RT,LT = ...

    # map controller values from -40 to +40, no decimals...
    # Eventually build in way to control this value.

    MotorControl(RX,RY,LX,LY,RT,LT)

    temp,pressure = ReadSensors()

    # Sital PID controller

    












