# PID Controller Implementation for ROV
# This is a barebones code, cannibalized from an online source,
# sought to used as a platform for future iterations of PID Code
# UNH ROV

import time

class PID:
    """
    Implementation of a simple PID Control. All gain values are intitally set to 0
    """
    
    # Function to intialize PID gains
    def gain_init(self):
        self.Kp = 0
        self.Ki = 0
        self.Kd = 0

        self.Initialize()

    # Set P gain
    def setKp(self):
        self.Kp = input("Please Enter P gain value: ")

    # Set I gain
    def setKi(self):
        self.Ki = input("Please Enter I gain value: ")

    # Set D gain
    def setKd(self):
        self.Kd = input("Please Enter D gain value: ")

    # Set Previous Iteration Error
    def setPrevError(self, preverror):
        self.prev_error =  preverror

    # Initailize function
    def Initialize(self):
        # Initialization of delta-t variables
        self.currenttime = time.time()
        self.previoustime = self.currenttime

        # Initailize previous error
        self.prev_error = 0

        # Term result variables
        self.Cp = 0
        self.Ci = 0
        self.Cd = 0

    def GenOut(self, error):
        """
        Performs PID computation and returns control value based on elapsed time (dt) and the
        error signal from a summing junction (the error parameter)
        """

        self.currenttime = time.time()                  # Retrieve t
        dt = self.currenttime - self.previoustime       # Retrieve dt
        d_error = error - self.prev_error               # Obtain delta error (de)

        self.Cp = self.Kp * error                       # Proportional Term
        self.Ci += error * dt                           # Integral Term

        self.Cd = 0
        if dt > 0:                                      # Prevents division by 0
            self.Cd = d_error/dt                        # Derivative Term

        self.previoustime = self.currenttime            # Save t for next iteration
        self.prev_error = error                         # Save previous error

        # Sum and return PID value
        PID = self.Cp + (self.Ki + self.Ci) + (self.Kd + self.Cd)
        return PID
    
        
        
