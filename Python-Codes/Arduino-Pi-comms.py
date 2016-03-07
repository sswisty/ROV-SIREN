## Arduino - Pi comms test

import time
import serial
import random


arduino = serial.Serial('/dev/ttyACM0',115200)



while True:
    test1 = random.randint(0, 10)
    test2 = random.randint(0, 100) # Create random integers to send to arduino

    arduino.write(str(test1).encode())
    arduino.write(str(test2).encode())

    print 'Sent: ',test1, test2

    bytesToRead = arduino.inWaiting()
    yaw = arduino.read(bytesToRead)

    bytesToRead = arduino.inWaiting()
    pitch = arduino.read(bytesToRead)

    bytesToRead = arduino.inWaiting()
    roll = arduino.read(bytesToRead)

    print 'Yaw: ', yaw
    print 'Pitch: ',pitch
    print 'Roll: ', roll

    
