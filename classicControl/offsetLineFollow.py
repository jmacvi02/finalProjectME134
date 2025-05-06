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
        self.state_vector = [] #[bottomX, bottomY, topX, topY] when populated

        self.state = "idle"

        self.center = 70 #pick center in horizontal middle?
        self.kp = 0.1 #PID values for line following
        self.ki = 0.000
        self.kd = 0.05
        self.baseVelL = 35 #higher base vel to account for the extra weight of the camera mount
        self.baseVelR = 30

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
        
    def transition(self):
        if self.lineDetect():
            print(f"{self.state_vector[0]}, {self.state_vector[1]}, {self.state_vector[2]}, {self.state_vector[3]}")
            if self.state_vector[2] == self.state_vector[0]:
                slope = 100
            else:
                slope = (self.state_vector[3] - self.state_vector[1]) / (self.state_vector[2] - self.state_vector[0])

            print(f"slope: {slope}")
            if (abs(slope) < 1): 
                self.state = "straightAway"
            elif (abs(slope) >= 1):  
                self.state = "turn"
        else:
            self.state = "idle"

    def execute(self):
        if self.state == "idle":
            print(f"idle")
            self.diffDrive.stop()
        elif self.state == "straightAway":
            newVel = self.straightAway()
            print("straight")
            self.diffDrive.set_speed(self.baseVelL - newVel, self.baseVelR + newVel)
        elif self.state == "turn":
            newVel= self.turn()
            print("turn")
            self.diffDrive.set_speed(self.baseVelL - newVel, self.baseVelR + newVel)

    def straightAway(self):
        #accounting for arrow pointing right 
        if self.state_vector[0] < self.state_vector[2]:
            error = self.center-self.state_vector[3]
            self.intError += error
            self.derError = error - self.prevError
            newEffort = error*self.kp + self.derError*self.kd + self.intError*self.ki
    
            return newEffort
        #accounting for arrow pointing left 
        else:
            error = self.center-self.state_vector[1]
            self.intError += error
            self.derError = error - self.prevError
            newEffort = error*self.kp + self.derError*self.kd + self.intError*self.ki
    
            return newEffort
        
    def turn(self):
        
        return 12



