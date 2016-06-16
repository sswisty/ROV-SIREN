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
import smbus

from SendReceive import SendReceive

import time     # may not be necessary for final build

# ===================================================================
#    ----------------- Inatilization commands ----------------

# Define the hat and the pressure sensor over the I2C connection pins
hat = PWM(0x40)
bus = smbus.SMBus(1)

# Set the desired frequency for the servos (50 Hz)
f = 48
hat.setPWMFreq(f)

# Define the thruster pins on the ServoHat
global thruster1
global thruster2
global thruster3
global thruster4
global thruster5
global thruster6

# Sital, may have to reorder these to account for everything (LIGHT and CLAW)
thruster1 = 0;
thruster2 = 2;
thruster3 = 4;
thruster4 = 6;
thruster5 = 8;
thruster6 = 10;
thruster7 = 12;
thruster8 = 14;
LED = 15;
Claw = 16;


center = 307    # Use this to initilize the thrusters

brightness = 0  # Brightness of LED (0-800-1600 microseconds)
led_inc = 800   # used to go up and down increments of 800 microseconds

# MS5837_30BA01 address, 0x76(118)
#		0x1E(30)	Reset command
bus.write_byte(0x76, 0x1E)



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



# ====================================================================
#    ------------------ Main Loop -----------------------

while True:

    # Read pressure and sensor, UDP code works by sending message first
    Pressure, Temp = ReadTempPressure()
    
    # Communication with PC
    # Read in game controller values
    LX,LY,RX,RY,LT,RT,PadUD,PadLR = SendReceive(Pressure, Temp)  # get d-pad values also...

    # Use controller values to control thrusters
    MotorControl(RX,RY,LX,LY,RT,LT)

    print LX, LY, RX, RY, LT, RT


    # Toggle Light (D-Pad UP/DOWN to go up/down 3 levels of brightenss)
    if PadUD == 1:
        brightness += led_inc
    if PadUD == -1:
        brightness -= led_inc

    if brightness > 1600:
        brightness = 1600
    if brightness < 0:
        brightness = 0

    hat.setPWM(LED,0,brightness) # sets PWM to brightness setting

    
    

    # Sital PID controller


# END OF MAIN LOOP

#===============================================================================
#        OTHER FUNCTIONS I WAS TOO LAZY TO WRITE IN ITS OWN .py FILE (sorry)
#           ALSO COMMENTS ABOUT HOW THE CODE WORKS AND CAN BE MODIFIED
#===============================================================================

# SITAL, I am going to assume that everything here is correct. I am also going
# to have the function return Temp and Pressure to use in the main loop above.
# Elimaniting (comment out) the time.sleep() for now, dont want the loop to
# stall during driving...
def ReadTempPressure():
    # Read 12 bytes of calibration data
    # Read pressure sensitivity
    data = bus.read_i2c_block_data(0x76, 0xA2, 2)
    C1 = data[0] * 256 + data[1]

    # Read pressure offset
    data = bus.read_i2c_block_data(0x76, 0xA4, 2)
    C2 = data[0] * 256 + data[1]

    # Read temperature coefficient of pressure sensitivity
    data = bus.read_i2c_block_data(0x76, 0xA6, 2)
    C3 = data[0] * 256 + data[1]

    # Read temperature coefficient of pressure offset
    data = bus.read_i2c_block_data(0x76, 0xA8, 2)
    C4 = data[0] * 256 + data[1]

    # Read reference temperature
    data = bus.read_i2c_block_data(0x76, 0xAA, 2)
    C5 = data[0] * 256 + data[1]

    # Read temperature coefficient of the temperature
    data = bus.read_i2c_block_data(0x76, 0xAC, 2)
    C6 = data[0] * 256 + data[1]

    # MS5837_30BA01 address, 0x76(118)
    #		0x40(64)	Pressure conversion(OSR = 256) command
    bus.write_byte(0x76, 0x40)

    # time.sleep(0.5)

    # Read digital pressure value
    # Read data back from 0x00(0), 3 bytes
    # D1 MSB2, D1 MSB1, D1 LSB
    value = bus.read_i2c_block_data(0x76, 0x00, 3)
    D1 = value[0] * 65536 + value[1] * 256 + value[2]

    # MS5837_30BA01 address, 0x76(118)
    #		0x50(64)	Temperature conversion(OSR = 256) command
    bus.write_byte(0x76, 0x50)

    time.sleep(0.5)

    # Read digital temperature value
    # Read data back from 0x00(0), 3 bytes
    # D2 MSB2, D2 MSB1, D2 LSB
    value = bus.read_i2c_block_data(0x76, 0x00, 3)
    D2 = value[0] * 65536 + value[1] * 256 + value[2]

    dT = D2 - C5 * 256
    TEMP = 2000 + dT * C6 / 8388608
    OFF = C2 * 65536 + (C4 * dT) / 128
    SENS = C1 * 32768 + (C3 * dT ) / 256
    T2 = 0
    OFF2 = 0
    SENS2 = 0

    if TEMP >= 2000 :
            T2 = 2 * (dT * dT) / 137438953472
            OFF2 = ((TEMP - 2000) * (TEMP - 2000)) / 16
            SENS2 = 0
    elif TEMP < 2000 :
            T2 = 3 *(dT * dT) / 8589934592
            OFF2 = 3 * ((TEMP - 2000) * (TEMP - 2000)) / 2
            SENS2 = 5 * ((TEMP - 2000) * (TEMP - 2000)) / 8
            if TEMP < -1500 :
                    OFF2 = OFF2 + 7 * ((TEMP + 1500) * (TEMP + 1500))
                    SENS2 = SENS2 + 4 * ((TEMP + 1500) * (TEMP + 1500))

    TEMP = TEMP - T2
    OFF2 = OFF - OFF2
    SENS2 = SENS - SENS2
    pressure = ((((D1 * SENS2) / 2097152) - OFF2) / 8192) / 10.0
    cTemp = TEMP / 100.0
    fTemp = cTemp * 1.8 + 32

    return pressure, cTemp












