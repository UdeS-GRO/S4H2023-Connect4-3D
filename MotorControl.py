#Alexandre Baril, 17 janvier 2023, Sherbrooke

import struct
#import numpy as np

BicepLen = 150
ForearmLen = 150

def cart2cyl(cartX, cartY):
    C2 = (cartX**2 + cartY**2 - BicepLen**2 - ForearmLen**2) / (2 * BicepLen * ForearmLen)
    S2 = (1-C2) ** 0.5
    theta = 5 #cos(C2)     ###cos-1 à impléementer!!!
    phi = 10 #atan2((ForearmLen * S2 * cartX) + ((BicepLen + ForearmLen*C2)*cartY), ((BicepLen + ForearmLen*C2)*cartX)-(ForearmLen * S2 * cartY))
    #print([theta, phi])
    return [theta, phi]

def deg2Servo(angleDeg):
    angleServo = angleDeg * 4096 / 360
    return angleServo

def Interpolation(posXStart, posYStart, posXEnd, posYEnd):
    jointAngles = cart2cyl(posXStart, posYStart)
    posx = posXStart
    posy = posYStart
    diffX = posXEnd - posXStart
    diffY = posYEnd - posYStart

    while posx != posXEnd and posy != posYEnd:
        cart2cyl(posx, posy)
        posx += (diffX/20)
        posy += (diffY/20)
        jointAngles = cart2cyl(posx, posy)
        jointAngles[0] = deg2Servo(jointAngles[0])
        jointAngles[1] = deg2Servo(jointAngles[1])
        print(jointAngles)
    return jointAngles

def moveZ(height, direction):
    #1 = down
    #0 = up
    #while encoderValue != range(height-50, height+50):
    #    #motor.move(direction, speed, etc)
    #    print(encoderValue)

    print("height = " + height)
    return

#sends the 3 motor positions to the openCR board

##### MAIN #####

#receive from OpenCR card:
    #encodervalue, motorShoulderposition, motorElbowposition

#dataPack = struct.pack('iii', encodervalue, motorShoulderPosition, motorElbowPosition)
#data = struct.unpack('iii', dataPack)

#sends to OpenCR
motorMvt = Interpolation(100, 50, 200, 150)
motorShoulder = motorMvt[0]
elbowShoulder = motorMvt[1]

print(motorShoulder)
print(elbowShoulder)

print("hello")