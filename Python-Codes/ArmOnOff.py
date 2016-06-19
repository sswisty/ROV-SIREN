#Servo Arm On

from Adafruit_PWM_Servo_Driver import PWM
import time

# Initialize PWM device through default address
pwm = PWM(0x40)

armopen_p = 350
armclose_p = 500
armclose_f = 700

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   
  pulseLength /= 60                       
  print "%d us per period" % pulseLength
  pulseLength /= 4096                    
  print "%d us per bit" % pulseLength
  pulse *= 100
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)    

pwm.setPWMFreq(60)

pwm.setPWM(0, 0, armopen_p) # Initailizes arm so it starts in open position

while (True):
    status = input("Arm Status (Arm Closed = 1, Arm Opened = 0): ")
    if status == 1:
        pwm.setPWM(0, 0, armclose_p) # Opens Arm
        print "Armature Opened!"
    if status == 0:
        pwm.setPWM(0, 0, armopen_p) # Partially Closes Arm
        print "Armature Partially Closed!"
    if status == 2:
        pwm.setPWM(0, 0, armclose_f) # Fully Closes Arm
        print "Armature Fully Closed!"
    if status != 1 and status != 0:
        status = input("Error! Please enter valid command (Arm Closed = 1, Arm Opened = 0): ")
    
        




