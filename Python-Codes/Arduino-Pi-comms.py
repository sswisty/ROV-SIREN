## Arduino - Pi comms test

import time
import serial
import random


arduino = serial.Serial('/dev/ttyACM0',115200)

def SendData(value):
    arduino.write(value)
    #arduino.write(str(value2).encode())
     
    
def ReadData():
    bytesToRead = arduino.inWaiting()
    data = arduino.readline(bytesToRead)
    if data != '':
        data = int(data)
    return data
    


while True:
    
    test1 = random.randint(0, 10)
    test2 = random.randint(0, 100) # Create random integers to send to arduino

    test1 = str(test1)
    test2 = str(test2)
    data = str(test1 + ',' + test2)
    SendData(data)
    

    print 'Sent: ',test1, test2

    time.sleep(.25)

    yaw = ReadData()
    pitch = ReadData()
    roll = ReadData()


    print 'Yaw: ', yaw
    print 'Pitch: ', pitch
    print 'Roll: ', roll

    print ' \n' 

    #time.sleep(.75)

    
