# UNH ROV
# Raspberry Pi Servo Control Test Code

# =================================================================

# Necessary libraries
from Adafruit_PWM_Servo_Driver import PWM
import time     # may not be necessary for final build

# Define the hat over the I2C connection pins
hat = PWM(0x40)

# Set the desired frequency for the servos (400 Hz)
f = 400
hat.setPWMFreq(f)


# ================== CONTROLL THRUSTERS ============================

# Deadzone is 1500 microseconds. Calculate the tic number and store as center
f = 400.00000        # decimals force precision

center = 1500        # microseconds

pulsetime = 1/f      # length of pulse (s)
pulsetime *= 1000    # length of pulse (ms)

tictime = pulsetime/4096    # time of each tic (ms)
tictime *= 1000             # time of each tic (microseconds)

center /= tictime           # set center to tic of 1100 microseconds


# Define the thruster channels
thruster1 = 0


# make a loop to change the thrust value
while (True):
    
    hat.setPWM(thruster1, 0, center)
    print "Thruster stopped \n"
    time.sleep(1.5)
    
    hat.setPWM(thruster1, 0, center+75)
    print "Thruster forward! \n"
    time.sleep(3)
    
    hat.setPWM(thruster1, 0, center)
    print "Thruster stopped \n"
    time.sleep(1.5)
    
    hat.setPWM(thruster1, 0, center-75)
    print "Thruster forward! \n"
    time.sleep(3)



    
