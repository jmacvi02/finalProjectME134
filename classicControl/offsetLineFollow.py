# Author:       Joel MacVicar
# Date Updated: 5/7/2025
# Name :        offsetLineFollow.py
# Purpose:      A offset line following class to control the XRP around a rectangular track.
#               This control class uses the Husky lens to detect a line along the top of the 
#               inner wall of the the track. It uses a PD controller to follow both a target
#               slope and position of the line. 

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
        self.state = "searching"

        self.slope = 0 #initial
        self.center = 80 #the target y position of the line
        self.baseVelL = 35 #higher base vel to account for the extra weight of the camera mount
        self.baseVelR = 30
        self.kSP = 10
        self.kPP = 0.1
        self.kSD = 0  #   5
        self.kPD = 0  #  0.07
        self.slopeErrorPrev = 0
        self.posErrorPrev = 0

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
        """
        Determines if the robot needs to transition states.
        """
        if self.state == "lineFollowing":
            if not self.lineDetect():
                self.state = "searching"
        elif self.state == "searching":
            if self.lineDetect():
                self.state = "lineFollowing"

    def execute(self):
        """
        Executes control based on the current state
        """
        if self.state == "lineFollowing":
            newVel = self.lineFollow()
            #print("following")
            self.diffDrive.set_speed(self.baseVelL - newVel, self.baseVelR + newVel)
        elif self.state == "searching":
            #print("searching")
            self.diffDrive.set_speed(10, 30)

        #small sleep to allow for change to occur before calling state transition
        time.sleep(0.05)

    def lineFollow(self):
        """
        PD line following control using the Husky Lens. Cannot be run on its own since state_vector is updated by lineDetect function.

        :return: the calculated velocity to be added/subtracted from the base velocity
        :rtype: float
        """        
        #accounting for a completely vertical line (which has infinite slope)
        if self.state_vector[2] == self.state_vector[0]:
            self.slope = 10
        else:
            self.slope = (self.state_vector[3] - self.state_vector[1]) / (self.state_vector[2] - self.state_vector[0])

        #error and derivative error calculations
        slopeError = -self.slope
        posError = self.center - (self.state_vector[3] + self.state_vector[1])/2
        derSlopeError = slopeError - self.slopeErrorPrev
        derPosError = posError - self.posErrorPrev
        #updates prev errors to current error
        self.slopeErrorPrev = slopeError
        self.posErrorPrev = posError
        #new velocity calculation
        newVel = (self.kSP*slopeError + self.kSD*derSlopeError) + (self.kPP * posError + self.kPD*derPosError)
    
        return newVel




