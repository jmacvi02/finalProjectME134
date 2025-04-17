
import math



#
# Eli this returns the magnitude and the angle if you give it the current x and y postions you get from joy stick
#

def joyToMagAng(absX, absY):
    centX = #offset val ELI PUT THE X VALUE AT CENTER HERE
    centY = #offset val ELI PUT THE Y VALUE AT  CENTER HERE

    relX = absX - centX
    relY = absY = centY

    mag = math.sqrt(relX**2 + relY**2)
    #quadrant 1
    if relX > 0 and relY > 0:
        angle = (math.pi/2) - math.atan2(relY, relX)
    #quad 2
    elif relX < 0 and relY > 0:
        angle = (math.pi/2) - math.atan2(relY, abs(relX))
    #quad 3
    elif relX < 0 and relY < 0:
        angle = (math.pi)/2 + math.atan2(abs(relY), abs(relX))
    #quad 2
    elif relX > 0 and relY > 0:
        angle = -math.pi - math.atan2(abs(relY), relX)

    return mag, angle


#
# ELI this returns the efforts to send to the motor if you give it the magnitude and angle 
#
def mapToEffort(mag, angle):
    maxMAG = #ELI PUT WHATEVER THE MAGNITUDE IS WHEN JOY STICK IS ALL THE WAY EXTENDED HERE

    magFactor = 1 / maxMag
    effortMag = mag * magFactor

    if abs(angle) <= ((3* math.pi) / 4):
        turnFactor = 0.5 / ((3* math.pi) / 4)
        effortAngle = angle * turnFactor
        effortL = effortMag - effortAngle
        effortR = effortMag + effortAngle
    if angle == 0:
        effortL = effortMag
        effortR = effortMag    

    if abs(angle) > ((3* math.pi) / 4):
        turnFactor = (0.25/ math.pi)
        effortAngle = (math.pi - angle) * turnFactor
        effortL = (-effortMag / 4) + effortAngle
        effortR = (-effortMag / 4) - effortAngle


    return effortL, effortL

