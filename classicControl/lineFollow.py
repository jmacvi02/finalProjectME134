from XRPLib.differential_drive import DifferentialDrive
from Husky.huskylensPythonLibrary import HuskyLensLibrary

import time

class lineFollow:
    def __init__(self, ):
        self.husky = HuskyLensLibrary("I2C")
        # Ensure HuskyLens is in line tracking mode
        while not self.husky.line_tracking_mode():
            self.husky.line_tracking_mode()  
        self.diffDrive = DifferentialDrive.get_default_differential_drive()
        self.state_vector = []

        self.center = 160
        self.kp = 0.002 #PID values for line following
        self.ki = 0.0001
        self.kd = 0.0007
        self.effort = 0.5

        self.prevError = 0
        self.derError = 0
        self.intError = 0

    def lineDetect(self):
        """
        Determines if there is a line for the XRP to follow

        :return: returns True if there is a line to follow, and False if there is no line. 
        :rtype: bool
        """
        
        state = self.husky.command_request_arrows_learned()

        if len(state) > 0:
            self.state_vector = state[0]

            return True
        else:
            return False

    def PIDLineFollow(self):
        """
        Follows the line which the Husky camera is trained to identify
        """
        # x1 and x2 are the left and right points of the arrow
        state_x2 = self.state_vector[2]  # grab the front of the arrow from the camera

        if state_x2 <= 41 and self.prevError < -75: # account for the weird pixel mapping in the right of camera
            state_x2 += 248
        error = self.center - state_x2
        self.derError = error - self.prevError
        self.intError = min(self.intError+ error, 0.1) #account for the bad surface causing caster wheels to stick
        self.prevError = error

        newEffort = error*self.kp + self.derError*self.kd + self.intError*self.ki

        self.diffDrive.set_effort(self.effort-newEffort, self.effort+newEffort)

        print(f"X2: {state_x2}")
        time.sleep(0.1)



