# Function to initialize and run depth control for ROV-005 "Siren"
# Written by: Sital Khatiwada

import smbus
import time

def depthcontrol(pressure):

    # Note: Pressure is given as mbar, must convert to psi (lbs/ft^2)

    pressure = pressure * 2.0885434273 # Conversion from mbar to lbs/ft^2

    des_depth = input

    g = 32.2 # Gravity in ft/s^2

    rho = 62.301 # Density of water @ 70F

    depth_rov = pressure/(g*rho) # Depth of Siren through hydrostatic equation

    if depth_rov > des_depth:

        # Fire thrusters up!

    if depth_rov < des_depth:

        # Fire thrusters down

    if depth_rov < des_depth - .5 or depth_rov > des_depth + .5:

        # Turn thrusters off

