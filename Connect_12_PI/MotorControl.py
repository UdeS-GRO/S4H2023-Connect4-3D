## Class: MotorMove
## Summary: This class is used to send messages to the OpenCR board. When other classes call
##          the sendMsg method, the joint positions are updated and are sent to the OpenCR board.

import struct
import numpy as np
import serial
import time
import sys
import serial.tools.list_ports
from PyQt5 import QtWidgets
app = QtWidgets.QApplication(sys.argv)
# from GameBoardRepresentation import gameboard
# game = gameboard()

theta = 0.001
phi = 0.001


class MotorMove:
    # Math variable
    BicepLen: float = 0.1425
    ForearmLen: float = 0.1425
    J1Offset: int = 0
    J2Offset: int = 0

    # Communication variables
    mssg1: str = "0000"
    mssg2: str = "0000"
    mssg3: str = "0000"
    mssg4: str = "0"  # default is go to 45deg
    mssg5: str = "3"  # default is reset of all magazines
    mssg6: str = "0"  # default is not resetSequence
    mssg7: str = "0"  # default is no victory
    mssg: str = "0000000000000000"

    Zpos: int = 0  # zposition

    # serOpenCR = serial.Serial('/dev/ttyUSB0', 9600)        #Linux or Pi
    serOpenCR = serial.Serial('COM3', baudrate=9600, timeout=2.0)  # Windows

    # Methods
    def __init__(self):
        self.init_motor(self)

    def sendMsg(self, Shouldermessage: int, Elbowmessage: int):
        #Shouldermessage = joint 1 (angle from 0 to 4095)
        #Elbowmessage = joint 2 (angle from 0 to 4095)
        #all the other messages are updated externaly with MotorMove.mssg4 = "1" or MotorMove.zpos = 1000 for exemple.

        '''
        communication order:    [j1 j1 j1 j1  --> int 0-9 times 4
                                j2 j2 j2 j2   --> int 0-9 times 4
                                z z z z       --> int 0-9 times 4
                                Pos to go     --> int 0 = 45deg, 1 = 90deg
                                Pos to reset  --> int 0 = nothing, 1 = 45deg, 2 = 90deg
                                ]
        ex: 01230123012300
        '''
        print("Sending message")

        #The next block of code is used to make sure that the three joint positions are always 4 digits long.

        # First Joint Position
        Shoulderlength = len(str(Shouldermessage))
        if Shoulderlength == 1:
            mssg1 = "000" + str(Shouldermessage)
        elif Shoulderlength == 2:
            mssg1 = "00" + str(Shouldermessage)
        elif Shoulderlength == 3:
            mssg1 = '0' + str(Shouldermessage)
        elif Shoulderlength == 4:
            mssg1 = str(Shouldermessage)
        if mssg1 == "":
            mssg1 = "0000"

        # Second Joint Position
        Elbowlength = len(str(Elbowmessage))
        if Elbowlength == 1:
            mssg2 = "000" + str(Elbowmessage)  # + '|'
        elif Elbowlength == 2:
            mssg2 = "00" + str(Elbowmessage)  # + '|'
        elif Elbowlength == 3:
            mssg2 = '0' + str(Elbowmessage)  # + '|'
        elif Elbowlength == 4:
            mssg2 = str(Elbowmessage)  # + '|'
        if mssg2 == "":
            mssg2 = "0000"

        # Z Position
        Zlength = len(str(self.Zpos))
        if Zlength == 1:
            mssg3 = "000" + str(self.Zpos)  # + '|'
        elif Zlength == 2:
            mssg3 = "00" + str(self.Zpos)  # + '|'
        elif Zlength == 3:
            mssg3 = '0' + str(self.Zpos)  # + '|'
        elif Zlength == 4:
            mssg3 = str(self.Zpos)  # + '|'
        if mssg3 == "":
            mssg3 = "0000"        

        mssg = mssg1 + mssg2 + mssg3 + self.mssg4 + self.mssg5 + self.mssg6 + self.mssg7
        print(mssg)
        if self.serOpenCR.isOpen():
            self.serOpenCR.write(mssg.encode().rstrip())
            print("msg Sent: " + mssg+"\n")

        self.mssg5 = "0"
        self.mssg7 = "0"
        return

    def moveJoint(self, J1, J2):
        self.sendMsg(self, J1, J2)

    def sendVictory(self, winner):
        # this method is used to send the winner of the game to the OpenCR board
        # 3 = New Game, 1 = player, 2 = robot
        print("Winner is: ")
        if winner == 3:
            self.mssg7 = "3"
            self.sendMsg(self, 0, 0)
        elif winner == 1:
            self.mssg7 = "1"
            self.sendMsg(self, 0, 0)
        elif winner == 2:
            self.mssg7 = "2"
