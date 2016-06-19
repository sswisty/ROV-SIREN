#-----------------------------------------------------------------------------
# Blue Robotics Lumen Light
# **This script allows for the light source to be manually turned on and off**
# Wrtitten by: Sital Khatiwada
#-----------------------------------------------------------------------------

from Adafruit_PWM_Servo_Driver import PWM
import time

# Initialize PWM device through default address
pwm = PWM(0x40)

lighton = 1700
lightoff = 0

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   
  pulseLength /= 60                       
  print "%d us per period" % pulseLength
  pulseLength /= 4096                    
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)    

pwm.setPWMFreq(60)

while (True):
    status = input("Light Status (ON = 1, OFF = 0): ")
    if status == 1:
        pwm.setPWM(0, 0, lighton)
    if status == 0:
        pwm.setPWM(0, 0, lightoff)
        
