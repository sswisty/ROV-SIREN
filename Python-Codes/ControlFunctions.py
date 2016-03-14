

def MotorControl(RX,RY,LX,LY,RT,LT):

    # ================ XY Plane Motion =========================

    if (RX == 0):  # No Yaw control
        if (LY != 0 and LX == 0):
            # Only Forward/Backward
            WriteMotor(thruster1, LY)
            WriteMotor(thruster2, LY)
            WriteMotor(thruster3, LY)
            WriteMotor(thruster4, LY)
        elif (LY == 0 and LX != 0):
            # Only Left/Right
            WriteMotor(thruster1, LX)
            WriteMotor(thruster2, -LX)
            WriteMotor(thruster3, LX)
            WriteMotor(thruster4, -LX)
        else:
            # X and Y plane motion
            WriteMotor(thruster1, Correction(LY, LX, '+'))
            WriteMotor(thruster2, Correction(LY, LX, '-'))
            WriteMotor(thruster3, Correction(LY, LX, '+'))
            WriteMotor(thruster4, Correction(LY, LX, '-'))
            
    elif (RX != 0):   # Yaw Control
        if (LY == 0 and LX == 0):
            # Only Yaw (CW and CCW)
            WriteMotor(thruster1, RX)
            WriteMotor(thruster2, -RX)
            WriteMotor(thruster3, -RX)
            WriteMotor(thruster4, RX)
        elif (LY != 0 and LX == 0):
            # Yaw and Forward/Backward
            WriteMotor(thruster1, Correction(LY, RX, '+'))
            WriteMotor(thruster2, Correction(LY, RX, '-'))
            WriteMotor(thruster3, Correction(LY, RX, '-'))
            WriteMotor(thruster4, Correction(LY, RX, '+'))
        elif (LY == 0 and LX != 0):
            # Yaw and Left/right
            WriteMotor(thruster1, )
            WriteMotor(thruster2, )
            WriteMotor(thruster3, )
            WriteMotor(thruster4, )
        elif (LY != 0 and LX != 0):
            # Yaw and general XY Plane motion...
            #NOT CURRENTLY DOING THIS! Instead general xy-motion
            WriteMotor(thruster1, Correction(LY, LX, '+'))
            WriteMotor(thruster2, Correction(LY, LX, '-'))
            WriteMotor(thruster3, Correction(LY, LX, '+'))
            WriteMotor(thruster4, Correction(LY, LX, '-'))





def WriteMotor(Thruster, Value):
    # This writes the PWM setting to the ESC
    hat.setPWM(Thruster, 0, center + Value)



def Correction(value1, value2, sign):
    # For multi-axis motion we need to determine how much thrust each thruster
    # provides. One value is more important and thus provides a larger portion
    
    if (sign == '+'):
        correctvalue = value1/2 + (value1*value2)/80
    elif (sign == '-'):
        correctvalue = value1/2 - (value1*value2)/80

    return correctedvalue    
