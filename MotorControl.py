#Alexandre Baril, 17 janvier 2023, Sherbrooke

import struct
import numpy as np
import serial

BicepLen = float(150)
ForearmLen = float(150)

def rad2Servo(angleRad):
    angleServo = angleRad * 360 / (2*np.pi)
    return angleServo

def cart2cyl(cartX, cartY):
    C2 = (cartX**2 + cartY**2 - BicepLen**2 - ForearmLen**2) / (2 * BicepLen * ForearmLen)
    S2 = (1-C2) ** 0.5
    theta = np.arccos(C2)     ###cos-1
    phiX = (ForearmLen * S2 * cartX) + ((BicepLen + ForearmLen*C2)*cartY)
    phiY = ((BicepLen + ForearmLen*C2)*cartX)-(ForearmLen * S2 * cartY)
    phi = np.arctan2(((ForearmLen * S2 * cartX) + ((BicepLen + ForearmLen*C2)*cartY)), (((BicepLen + ForearmLen*C2)*cartX)-(ForearmLen * S2 * cartY)))

    theta = rad2Servo(theta)
    phi = rad2Servo(phi)

    return theta, phi

def Interpolation(posXStart: int, posYStart: int, posXEnd: int, posYEnd: int):
    jointAngles = cart2cyl(posXStart, posYStart)
    increment = 25
    posx = posXStart
    posy = posYStart
    diffX = posXEnd - posXStart
    diffY = posYEnd - posYStart
    stepX = diffX / increment
    stepY = diffY / increment
    
    positionsX = list()
    positionsY = list()
    jointAngles = list()
    for i in range(increment):
        positionsX.append(posXStart + (i+1)*stepX)
        positionsY.append(posYStart + (i+1)*stepY)
        #print("i: " + str(i) + "\tpositionX: " + str(positionsX[i]) + "  \tpositionY: " + str(positionsY[i]))
        jointAngles.append(cart2cyl(positionsX[i], positionsY[i]))
        #print("angle: " + str(jointAngles[i]))
    
    return positionsX, positionsY

def moveZ(height, direction):
    #1 = down
    #0 = up
    #while encoderValue != range(height-50, height+50):
    #    #motor.move(direction, speed, etc)
    #    print(encoderValue)

    print("height = " + height)
    return

def sendMsg():
    print("msg Sent!")
    return

##### SETUP #####
var = True
lastCoord = [0, 0]

##### MAIN #####
while var == True:
    #coordonates = import from jacob
    coord = [100, 150]

    #receive from OpenCR card:
        #encodervalue, motorShoulderposition, motorElbowposition
    #dataPack = struct.pack('iii', encodervalue, motorShoulderPosition, motorElbowPosition)
    #data = struct.unpack('iii', dataPack)

    #sends to OpenCR
    cartPosX, cartPosY = Interpolation(lastCoord[0], lastCoord[1], coord[0], coord[1])
    #print(cartPosX)
    #print(cartPosY)
    for pos in range(0, len(cartPosY)):
        motorShoulder, motorElbow = cart2cyl(cartPosX[pos], cartPosY[pos])
        #sendMsg motorShoulder
        #sendMsg motorElbow
        print("ShoulderAngle: " + str(motorShoulder) + "\t ElbowAngle: " + str(motorElbow))
        
    lastCoord = coord
    var = False
    