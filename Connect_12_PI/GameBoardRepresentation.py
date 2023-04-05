# Sandrine Gagne, February 1st 2023

import sys
import cv2
import pyzbar.pyzbar as pyzbar
import time
import os
from MotorControl import MotorMove
from PyQt5 import QtWidgets

from streak_counter import streak_counter
from UserInterface import userInterface


class gameboard(QtWidgets.QMainWindow):
    row_total = 4
    column_total = 4
    floor_total = 8
    board = []
    LastList = [0 for _ in range(16)]
    var = 0
    global cap

    def __init__(self):
        # Function used to display the user interface (UI) and let the user use inputs to move the robot
        # to a certain position or tell the program he's done playing.
        self.init_board()
        super().__init__()
        userInterface(self)

        # start camera
        # Create a VideoCapture object, validate if your PC's cam is 1 or 0 for index
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        return

    def init_board(self):
        # Uses the global variables to generate the gameboard matrix

        x = self.row_total
        y = self.column_total
        z = self.floor_total
        self.board = [[[0 for k in range(x)]
                       for j in range(y)] for i in range(z)]
        return

    def print_board(self):
        # Generate a visual representation of the gameboard to see what the robot / program knows of the game status.
        i = 1
        usermatrix = ('')
        for row in self.board:
            stringmatrix = ("\n\n                         A  B  C  D    floor = " + str(i) + "\n\n" + "1    " + str(row[0]) + "\n" + "2    " + str(
                row[1]) + "\n" + "3    " + str(row[2]) + "\n" + "4    " + str(row[3]))
            usermatrix = usermatrix + stringmatrix
            i += 1
        return usermatrix

    def print_stats(self):
        # Open the text file in read mode
        with open('Stats.txt', 'r') as f:
            # Read the values of the variables and convert them to integers
            VictoryHuman, VictoryRobot = map(int, f.readlines())
        return "Human Victory: " + str(VictoryHuman) + "\n" + "Robot Victory: " + str(VictoryRobot)

    def add_piece(self, position_list):
        # Display the piece played on the UI to refresh the gameboard.
        row = int(position_list[0])
        column = int(position_list[1])
        player_id = int(position_list[2])
        floor = self.determine_floor(row, column)
        if floor != None:
            self.board[floor - 1][row - 1][column - 1] = player_id
        return

    def delete_piece(self, row, column, floor):
        # Delete the piece played on the UI to refresh the gameboard.

        self.board[floor - 1][row - 1][column - 1] = 0
        return

    def determine_floor(self, row, column):
        # Calculate the actual floor of the piece, knowing the previous pieces played at this exact position.

        floor = 1
        row = int(row)
        column = int(column)
        for i in range(1, 7):
            if self.board[i - 1][row - 1][column - 1] != 0:
                floor = floor + 1
        return floor

    def detect_win(self, play):
        # Detect if there is a win on the gameboard.
        play = [int(play[0])]+[int(play[1])]+[int(play[2])]
        streaks = streak_counter(
            play, self.board, self.row_total, self.column_total, self.floor_total)
        print("streak", streaks)
        for streak in streaks:
            if int(streak) == 4:
                return True
        return False

    def start_new_game(self):
        # This function starts a completely new game
        print("New game started")
        self.init_board()
        self.LastList = [0 for _ in range(16)]
        MotorMove.mssg5 = "3"
        MotorMove.sendVictory(MotorMove, 3)
        self.label.setText(self.print_board())
        self.label2.setText(self.print_stats())
        return

    def resetPick45deg(self):
        # Move the robot to his pick position registered, where the pieces dispenser is placed at 45 deg
        if( MotorMove.mssg5 == "2"):
            MotorMove.mssg5 = "3"
            print("MotorMove.mssg5 = 3")
        else:
            MotorMove.mssg5 = "1"
            print("MotorMove.mssg5 = 1")
        return

    def resetPick90deg(self):
        # Move the robot to his pick position registered, where the pieces dispenser is placed at 0 deg
        if(MotorMove.mssg5 == "1"):
            MotorMove.mssg5 = "3"
            print("MotorMove.mssg5 = 3")
        else:
            MotorMove.mssg5 = "2"
            print("MotorMove.mssg5 = 2")
        return

    def move_button1_down(self):
        self.submit_button1.move(
            self.submit_button1.x(), self.submit_button1.y() + 5)

    def move_button1_up(self):
        self.submit_button1.move(
            self.submit_button1.x(), self.submit_button1.y() - 5)

    def move_button2_down(self):
        self.submit_button2.move(
            self.submit_button2.x(), self.submit_button2.y() + 5)

    def move_button2_up(self):
        self.submit_button2.move(
            self.submit_button2.x(), self.submit_button2.y() - 5)

    def move_button3_down(self):
        self.submit_button3.move(
            self.submit_button3.x(), self.submit_button3.y() + 5)

    def move_button3_up(self):
        self.submit_button3.move(
            self.submit_button3.x(), self.submit_button3.y() - 5)

    def move_button4_down(self):
        self.submit_button4.move(
            self.submit_button4.x(), self.submit_button4.y() + 5)

    def move_button4_up(self):
        self.submit_button4.move(
            self.submit_button4.x(), self.submit_button4.y() - 5)

    def submit_robot_pos(self, row, column, floor):
        # Returns the xyz coordinates of the position where the robot has to move to.
        # The xyz values are hard coded based on experimental moves. The values may changes according to the robot environment.
        # The reference position is A1 and then the other positinos are automatically generated.
        print("row: " + str(row) + " column: " +
              str(column) + " floor: " + str(floor))

        offsetJ1 = 250
        offestJ2 = 0

        # row = 123    column = abc

        if (row == 1 and column == 1):
            J1 = 1580 + offsetJ1
            J2 = 3900 + offestJ2
            PickPlace = 45
        elif (row == 1 and column == 2):
            J1 = 770 + offsetJ1
            J2 = 4095 + offestJ2
            PickPlace = 45
        elif (row == 1 and column == 3):
            J1 = 3161 + offsetJ1
            J2 = 916 + offestJ2
            PickPlace = 45
        elif (row == 1 and column == 4):
            J1 = 2560 + offsetJ1
            J2 = 1060 + offestJ2
            PickPlace = 45
        elif (row == 2 and column == 1):
            J1 = 1460 + offsetJ1
            J2 = 3720 + offestJ2
            PickPlace = 45
        elif (row == 2 and column == 2):
            J1 = 960 + offsetJ1
            J2 = 3810 + offestJ2
            PickPlace = 45
        elif (row == 2 and column == 3):
            J1 = 3045 + offsetJ1
            J2 = 1190 + offestJ2
            PickPlace = 45
        elif (row == 2 and column == 4):
            J1 = 2505 + offsetJ1
            J2 = 1320 + offestJ2
            PickPlace = 45
        elif (row == 3 and column == 1):
            J1 = 3360 + offsetJ1
            J2 = 1630 + offestJ2
            PickPlace = 90
        elif (row == 3 and column == 2):
            J1 = 3130 + offsetJ1
            J2 = 1545 + offestJ2
            PickPlace = 90
        elif (row == 3 and column == 3):
            J1 = 2780 + offsetJ1
            J2 = 1545 + offestJ2
            PickPlace = 45
        elif (row == 3 and column == 4):
            J1 = 2300 + offsetJ1
            J2 = 1650 + offestJ2
            PickPlace = 90
        elif (row == 4 and column == 1):
            J1 = 2655 + offsetJ1
            J2 = 2240 + offestJ2
            PickPlace = 45
        elif (row == 4 and column == 2):
            J1 = 2585 + offsetJ1
            J2 = 2030 + offestJ2
            PickPlace = 90
        elif (row == 4 and column == 3):
            J1 = 2290 + offsetJ1
            J2 = 2045 + offestJ2
            PickPlace = 45
        elif (row == 4 and column == 4):
            J1 = 1290 + offsetJ1
            J2 = 2787 + offestJ2
            PickPlace = 45
        else:
            J1 = 0
            J2 = 0
            PickPlace = 90
            print("Error: Invalid position")

        height_constant = -300
        height_init = 2350
        '''
        xA1Position = 0.111
        yA1Position = 0.110
        xgap = 0.056
        ygap = 0.056            # Use a negative value since the A1 position is at the top left

        if row == 1:
            xPosition = xA1Position
        elif row == 2:
            xPosition = xA1Position + xgap
        elif row == 3:
            xPosition = xA1Position + 2*xgap
        elif row == 4:
            xPosition = xA1Position + 3*xgap
        
        if column == 1:
            yPosition = yA1Position
        elif column == 2:
            yPosition = yA1Position + ygap
        elif column == 3:
            yPosition = yA1Position + 2*ygap
        elif column == 4:
            yPosition = yA1Position + 3*ygap
        '''
        zPosition = height_init + floor*height_constant
        if PickPlace == 45:
            MotorMove.mssg4 = "0"
        elif PickPlace == 90:
            MotorMove.mssg4 = "1"

        MotorMove.Zpos = zPosition
        # MotorMove.moveCart(MotorMove, xPosition, yPosition, zPosition)
        MotorMove.moveJoint(MotorMove, J1, J2)

        return J1, J2, zPosition

    def take_picture(self, player):
        # Take picture of the gameboard when the played button is press. Actualize the UI by comparing the actual status gameboard
        # and the previous status gameboard.

        start_time = time.time()
        list = self.LastList[:]
        # Capture a frame from the webcam
        while(True):
            ret, img = self.cap.read()
            if ret == True:
                break

        while list == self.LastList:
            i = 0
            # Capture a frame from the webcam
            while(True):
                ret, img = self.cap.read()
                if ret == True:
                    break

            # Crop the image and divise it into 16 squares
            center = (img.shape[1]//2, img.shape[0]//2)
            size = (1080-270, 1080-270)
            img = cv2.getRectSubPix(img, size, center)
            cv2.imshow("Webcam", img)                   # Show the frame

            # Exit the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            height, width, _ = img.shape
            square_size = (height//4, width//4)

            # Iterate through the rows and columns of the image
            for row in range(4):
                for col in range(4):
                    square = img[row*square_size[0]:(row+1)*square_size[0], col*square_size[1]:(
                        col+1)*square_size[1]]  # Extract each square of the image
                    gray_img = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)

                    qr_codes = pyzbar.decode(gray_img)  # Detect QR codes
                    for qr_code in qr_codes:            # Add QR code to the list
                        data = qr_code.data.decode()    # Get QR code data
                        if (player == 2 and int(data) < 47 or player == 4 and int(data) > 46):
                            list[i] = (int(data))
                    i += 1

            time.sleep(0.2)                             # Wait 0.2 seconds

        for i, (a, b) in enumerate(zip(list, self.LastList)):
            if a != b:
                x = i % 4+1
                y = i//4+1
                if (a < 47):
                    Player = 2
                else:
                    Player = 4

        self.LastList = list
        cv2.destroyAllWindows()

        return Player, x, y

    def StatsAddWin(self, Player):

        # Open the text file in read mode
        with open('Stats.txt', 'r') as f:
            # Read the values of the variables and convert them to integers
            VictoryHuman, VictoryRobot = map(int, f.readlines())

        if (Player == 1):
            VictoryHuman += 1
        elif (Player == 2):
            VictoryRobot += 1

        # Open the same text file in write mode
        with open('Stats.txt', 'w') as f:
            # Write the updated values of the variables to the file
            f.write(f"{VictoryHuman}\n{VictoryRobot}")

        # Close the file
        f.close()
