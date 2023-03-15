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
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)        # Create a VideoCapture object, validate if your PC's cam is 1 or 0 for index
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)         # Set the focus distance
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)        # Set the focus distance
        return
    
    def init_board(self):
        # Uses the global variables to generate the gameboard matrix

        x = self.row_total
        y = self.column_total
        z = self.floor_total
        self.board = [[[0 for k in range(x)] for j in range(y)] for i in range(z)]
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

    def detect_win(self,play):
        # Detect if there is a win on the gameboard.
        play = [int(play[0])]+[int(play[1])]+[int(play[2])]
        streaks = streak_counter(play,self.board,self.row_total,self.column_total,self.floor_total)
        for streak in streaks:
            if streak == 4:
                return True
        return False

    
    def submit_inputs_xyz(self):
        xPosition = self.line_edit3.text()
        yPosition = self.line_edit4.text()
        zPosition = self.line_edit5.text()
        MotorMove.Zpos = zPosition
        MotorMove.moveCart(MotorMove, int(xPosition), int(yPosition), int(zPosition))
        #print(str(int(xPosition)) + str(int(yPosition)) + str(int(zPosition)))
        return # int(xPosition), int(yPosition), int(zPosition)

    def actual_position_xyz(self):
        # Link with Alex's code 
        xActual = 1
        yActual = 2
        zActual = 2
        return xActual, yActual, zActual

    def actual_position_joints(self): # Receives the joints coordinates from the motor control program and uses it to display it on the UI.        
        # Link with Alex's code        
        # # Link with UI        
        joint1ActualPos = 1 
        joint2ActualPos = 2

        return joint1ActualPos, joint2ActualPos

    def submit_inputs_joints(self):
        # Send the joints coordinates entered from the UI to the motor control program, to move the robot to desired position.
        
        zPosition = self.line_edit5.text()
        joint1Position = self.line_edit6.text()
        joint2Position = self.line_edit7.text()
        MotorMove.Zpos = zPosition
        MotorMove.moveJoint(MotorMove, joint1Position, joint2Position)
        return int(joint1Position), int(joint2Position)

    def actual_position_joints(self):
        # Receives the joints coordinates from the motor control program and uses it to display it on the UI.

        # Link with UI
        joint1ActualPos = 1
        joint2ActualPos = 2
        return joint1ActualPos, joint2ActualPos

    def on_toggled(self, checked):
        if checked:
            self.toggle_button.setText("Automatic Mode")
        else:
            self.toggle_button.setText("Manual Mode")

        return

    def submit_auto_startSequence(self):
        # Starts the state machine to make the robot play

        MotorMove.mssg4 = "1"
        MotorMove.mssg5 = "0"

        return

    def submit_auto_resetSequence(self):
        # The robot stops its sequence and goes back home

        MotorMove.mssg6 = "1"

        return

    def submit_man_goToHome(self):
        # Move the robot to his home position registered

        MotorMove.mssg4 = "0"
        MotorMove.mssg5 = "0"

        return

    def submit_man_resetPick45deg(self):
        # Move the robot to his pick position registered, where the pieces dispenser is placed at 45 deg
        if MotorMove.mssg5 == "2" or MotorMove.mssg5 == "3":
            MotorMove.mssg5 = "3"
        else:
            MotorMove.mssg5 = "1"
        print("MotorMove.mssg5 = 1")
        return 

    def submit_man_resetPick90deg(self):
        # Move the robot to his pick position registered, where the pieces dispenser is placed at 0 deg
        if MotorMove.mssg5 == "1" or MotorMove.mssg5 == "3":
            MotorMove.mssg5 = "3"
        else:
            MotorMove.mssg5 = "2"
        return 

    def submit_man_goDown(self):
        # Move the z coordinate of the robot to its lower position

        MotorMove.mssg4 = "0"
        MotorMove.mssg5 = "3"

        return

    def submit_man_goToLS(self):
        # Move the z coordinate of the robot to its limit switch
                
        MotorMove.mssg4 = "0"
        MotorMove.mssg5 = "4"

        return 

    def submit_man_grip(self):
        # Activate the electromagnet
        
        MotorMove.mssg4 = "0"
        MotorMove.mssg5 = "5"

        return

    def submit_man_drop(self):
        # Disable the electromagnet
        
        MotorMove.mssg4 = "0"
        MotorMove.mssg5 = "6"

        return

    def update_selected_btn(self, btn):
        self.selected_btn = btn

    def update_selected_floor(self, floor):
        self.selected_floor = floor

    def submit_gameboard_pos(self):
        # Once a position and a floor is selected, the gameboard position is updated and the robot can move to this position.
        zPosition = self.line_edit5.text()
        cartX1Position = self.line_edit3.text()
        cartY2Position = self.line_edit4.text()
        MotorMove.mssg4 = "0"
        MotorMove.mssg5 = "2"
        MotorMove.moveCart(MotorMove, int(cartX1Position), int(cartY2Position), int(zPosition))

        if self.selected_btn and self.selected_floor:
            self.submit_robot_pos(self.selected_btn, self.selected_floor)

    def submit_robot_pos(self, row, column, floor):
        # Returns the xyz coordinates of the position where the robot has to move to. 
        # The xyz values are hard coded based on experimental moves. The values may changes according to the robot environment. 
        # The reference position is A1 and then the other positinos are automatically generated. 
        print("row: " + str(row) + " column: " + str(column) + " floor: " + str(floor))

        offsetJ1 = 40
        offestJ2 = 450

        if(row == 1 and column == 1):
            J1 = 1783 + offsetJ1
            J2 = 3523 + offestJ2
            PickPlace = 45
        elif (row == 1 and column == 2):
            J1 = 1082 + offsetJ1
            J2 = 3677 + offestJ2
            PickPlace = 45
        elif (row == 1 and column == 3):
            J1 = 3401 + offsetJ1
            J2 = 517 + offestJ2
            PickPlace = 45
        elif (row == 1 and column == 4):
            J1 = 2706 + offsetJ1
            J2 = 635 + offestJ2
            PickPlace = 45
        elif (row == 2 and column == 1):
            J1 = 3998 + offsetJ1
            J2 = 934 + offestJ2
            PickPlace = 45
        elif (row == 2 and column == 2):
            J1 = 3711 + offsetJ1
            J2 = 800 + offestJ2
            PickPlace = 45
        elif (row == 2 and column == 3):
            J1 = 3229 + offsetJ1
            J2 = 796 + offestJ2
            PickPlace = 90
        elif (row == 2 and column == 4):
            J1 = 2719 + offsetJ1
            J2 = 931 + offestJ2
            PickPlace = 45
        elif (row == 3 and column == 1):
            J1 = 3555 + offsetJ1
            J2 = 1250 + offestJ2
            PickPlace = 90
        elif (row == 3 and column == 2):
            J1 = 3307 + offsetJ1
            J2 = 1139 + offestJ2
            PickPlace = 45
        elif (row == 3 and column == 3):
            J1 = 2978 + offsetJ1
            J2 = 1155 + offestJ2
            PickPlace = 45
        elif (row == 3 and column == 4):
            J1 = 2567 + offsetJ1
            J2 = 1240 + offestJ2
            PickPlace = 90
        elif (row == 4 and column == 1):
            J1 = 2829 + offsetJ1
            J2 = 1897 + offestJ2
            PickPlace = 90
        elif (row == 4 and column == 2):
            J1 = 2828 + offsetJ1
            J2 = 1633 + offestJ2
            PickPlace = 90
        elif (row == 4 and column == 3):
            J1 = 2523 + offsetJ1
            J2 = 1660 + offestJ2
            PickPlace = 90
        elif (row == 4 and column == 4):
            J1 = 1987 + offsetJ1
            J2 = 1962 + offestJ2
            PickPlace = 90
        else:
            J1 = 0
            J2 = 0
            PickPlace = 90
            print("Error: Invalid position")
        
        height_constant = -300
        height_init = 2150
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
        #MotorMove.moveCart(MotorMove, xPosition, yPosition, zPosition)
        MotorMove.moveJoint(MotorMove, J1, J2)

        return J1, J2, zPosition

    def take_picture(self):
        # Take picture of the gameboard when the played button is press. Actualize the UI by comparing the actual status gameboard
        # and the previous status gameboard. 

        start_time = time.time()
        list = self.LastList[:]
     
        while list == self.LastList:
            i=0
            ret, img = self.cap.read()                       # Capture a frame from the webcam

            center = (img.shape[1]//2, img.shape[0]//2) # Crop the image and divise it into 16 squares
            size = (1080-300, 1080-300)
            img = cv2.getRectSubPix(img, size, center)
            cv2.imshow("Webcam", img)                   # Show the frame

            if cv2.waitKey(1) & 0xFF == ord('q'):       # Exit the loop if the 'q' key is pressed
                break

            height, width, _ = img.shape
            square_size = (height//4, width//4)

            for row in range(4):                        # Iterate through the rows and columns of the image
                for col in range(4):
                    square = img[row*square_size[0]:(row+1)*square_size[0], col*square_size[1]:(col+1)*square_size[1]]  # Extract each square of the image
                    gray_img = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)
                    
                    qr_codes = pyzbar.decode(gray_img)  # Detect QR codes
                    for qr_code in qr_codes:            # Add QR code to the list
                        data = qr_code.data.decode()    # Get QR code data
                        list[i]=(int(data))                
                    i+=1
            
            time.sleep(0.2)                             # Wait 0.2 seconds
        
        for i, (a, b) in enumerate(zip(list, self.LastList)):
            if a != b:
                x = i%4+1
                y = i//4+1
                if (a < 47):
                    Player = 2
                else:
                    Player = 4

        self.LastList = list
        cv2.destroyAllWindows()

        return Player, x, y
    
