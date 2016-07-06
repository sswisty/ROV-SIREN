# UNH ROV SIREN DRIVE CODE
# MATE 2016 - NASA NEUTURAL BUOYANCY LAB


# =========================================================
# Import libraries
import socket
import sys
from threading import Timer
import time
import select
from random import *
from Adafruit_PWM_Servo_Driver import PWM
from ControlFunctions import MotorControl, WriteMotor, Correction
import smbus

# =======================================================
# Initilization
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

brightness = 150  # Brightness of LED (0-800-1600 microseconds)
led_inc = 450   # used to go up and down increments of 800 microseconds

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
print "Hacking the Mainframe"
print "System Ready: Siren Primed"

Pressure = 0

Temp = 0
# ========================
# Pressure and Temperature readings
def ReadTempPressure():
##    time.sleep(0.5)
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

    time.sleep(0.25)

    # Read digital pressure value
    # Read data back from 0x00(0), 3 bytes
    # D1 MSB2, D1 MSB1, D1 LSB
    value = bus.read_i2c_block_data(0x76, 0x00, 3)
    D1 = value[0] * 65536 + value[1] * 256 + value[2]

    # MS5837_30BA01 address, 0x76(118)
    #		0x50(64)	Temperature conversion(OSR = 256) command
    bus.write_byte(0x76, 0x50)

    time.sleep(0.25)

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


# ==========================================================
# Communication
IP = "169.254.58.111"
port = 10070

PC_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = (IP, port)

print 'Starting up communication'

PC_socket.bind(server_address)
print 'Socket bound'

max_time = 15
PC_socket.setblocking(True)
print 'setblocking complete'

initialP,initialT = ReadTempPressure()
try:
    while True:
        print '\nWaiting to recieve command from master'

        did_timeout = True
        data_ready = select.select([PC_socket], [], [], max_time)
        if data_ready[0]:
            incoming, address = PC_socket.recvfrom(4096)
            incoming2, address2 = PC_socket.recvfrom(4096)
            incoming3, address3 = PC_socket.recvfrom(4096)
            incoming4, address4 = PC_socket.recvfrom(4096)
            incoming5, address5 = PC_socket.recvfrom(4096)
            incoming6, address6 = PC_socket.recvfrom(4096)
            incoming7, address7 = PC_socket.recvfrom(4096)
            incoming8, address8 = PC_socket.recvfrom(4096)
            incoming9, address9 = PC_socket.recvfrom(4096) 
	    print 'Recieved %s bytes from %s !' % (len(incoming), address)
            #LX, LY, RX, RY, LT, RT, DpadUD, DpadLR = incoming[:8]
            LX = int(float(incoming))
            LY = int(float(incoming2))
            RX = int(float(incoming3))
            RY = int(float(incoming4))
            LT = int(float(incoming5))
            RT = int(float(incoming6))
            DpadUD = int(float(incoming7))
            DpadLR = int(float(incoming8))#
            A = int(float(incoming9)) 
#LT, RT, DpadUD, DpadLR = incoming[5:8]
            print LX, LY, RX, RY, LT, RT, DpadUD, DpadLR
            did_timeout = False

            MotorControl(RX,RY,LX,LY,RT,LT)

            if DpadUD == 1:
                #close claw
                brightness = 700



		hat.setPWM(15,LED,brightness) 
            if DpadUD == -1:
                #open claw
		brightness = 150
                hat.setPWM(15,LED,brightness) 

        if not did_timeout:
            if incoming:
                print 'Attempting to send data...'
                if A == 1: 
			Pressure, Temp = ReadTempPressure()
		GagePressure = Pressure - initialP

		Depth =GagePressure*.401865/12 
                send_data = "Pressure(mbar): %s  Depth(ft): %s  Temperature(C): %s" % (Pressure,Depth, Temp)

                sent = PC_socket.sendto(send_data, address)

                print 'Sent %s bytes to %s' % (sent, address)

except KeyboardInterrupt:
    print 'User Cancled'
    pass
finally:
    PC_socket.close()

                






