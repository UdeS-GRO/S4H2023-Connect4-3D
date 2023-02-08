# Sandrine Gagne, February 1st 2023

import sys
import numpy as np
from tkinter import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import time
import os


class gameboard(QtWidgets.QMainWindow):
    row_total = 4
    column_total = 4
    floor_total = 6
    board = []
    LastList = [0 for _ in range(16)]
    
    def __init__(self):
        self.init_board()
        super().__init__()
        self.setWindowTitle("User Interface")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.label = QLabel("Gameboard")
        self.label.setText(self.print_board())
        self.label.setAlignment(Qt.AlignCenter)

        self.push_button1 = QCheckBox("PLAYER 1\nClick me when you've played")
        self.push_button1.clicked.connect(self.button_played)
        self.line_edit1 = QLineEdit()

        self.push_button2 = QCheckBox("PLAYER 2\nClick me when you've played")
        self.push_button2.clicked.connect(self.button_played)
        self.line_edit2 = QLineEdit()

        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.push_button1)
        self.left_layout.addWidget(self.line_edit1)

        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.push_button2)
        self.right_layout.addWidget(self.line_edit2)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.right_layout)

        self.central_widget.setLayout(self.main_layout)
        self.central_widget.setLayout(self.right_layout)
    
    def init_board(self):
        x = self.row_total
        y = self.column_total
        z = self.floor_total
        self.board = [[[0 for k in range(x)] for j in range(y)] for i in range(z)]
        return

    def print_board(self):
        i = 1
        usermatrix = ('')
        for row in self.board:
            stringmatrix = ("\n\n                         A  B  C  D    floor = " + str(i) + "\n\n" + "1    " + str(row[0]) + "\n" + "2    " + str(
                row[1]) + "\n" + "3    " + str(row[2]) + "\n" + "4    " + str(row[3]))
            usermatrix = usermatrix + stringmatrix
            i += 1
        return usermatrix

    def add_piece(self, position_list):
        row = int(position_list[0])
        column = int(position_list[1])
        player_id = int(position_list[2])
        limit_board = self.row_or_column_limit(row, column)
        if limit_board == 1:
            floor = self.determine_floor(row, column)
            if floor != None and limit_board == 1:
                self.board[floor - 1][row - 1][column - 1] = player_id
        return

    def delete_piece(self, row, column, floor):
        self.board[floor - 1][row - 1][column - 1] = 0
        return

    def row_or_column_limit(self, row, column):
        row = int(row)
        column = int(column)
        if row > 4 or column > 4:
            print('This case is not reachable. Try again.')
            self.add_piece(self.user_input_board())
            return 0
        return 1

    def determine_floor(self, row, column):
        floor = 1
        row = int(row)
        column = int(column)
        for i in range(1, 7):
            if self.board[i - 1][row - 1][column - 1] != 0:
                floor = floor + 1   
        if floor > 6:
            print('This case is not reachable. Try again.')
            self.add_piece(self.user_input_board())
            return None
        #else:
            #print('floor value is : ', floor)               
        return floor

    def detect_win(self,position_list):
        
        row_index = int(position_list[0])-1
        column_index = int(position_list[1])-1
        player_id = int(position_list[2])
        
        for i in range(self.floor_total):
                    if self.board[i][row_index][column_index] == 0:  
                        floor_index = i-1
                        break

        #Row verification
        streak = 0
        for i in range(0,self.row_total):
            if int(self.board[floor_index][i][column_index])==player_id:
                streak = streak + 1
                if streak == 4:
                    return True
            else:
                streak = 0
        #Column verification
        streak = 0
        for i in range(0,self.column_total):
            if int(self.board[floor_index][row_index][i])==player_id:
                streak = streak + 1
                if streak == 4:
                    return True
            else:
                streak = 0
        #Floor verification
        streak = 0
        for i in range(0,self.floor_total):
            if int(self.board[i][row_index][column_index])==player_id:
                streak = streak + 1
                if streak == 4:
                    return True
            else:
                streak = 0
        #Positive diagonal column and row verification
        streak = 0
        if row_index == column_index:
            for i in range(0,self.column_total):
                if int(self.board[floor_index][i][i])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Negative diagonal column and row verification
        streak = 0
        if row_index == self.column_total-1-column_index:
            for i in range(0,self.column_total):
                if int(self.board[floor_index][i][self.column_total-i-1])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Positive diagonal column and floor verification
        streak = 0
        gap = floor_index - row_index
        if row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if int(self.board[i+gap][i][column_index])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Negative diagonal column and floor verification
        streak = 0
        gap = floor_index - ((self.row_total-1)-row_index)
        if (self.row_total-1)-row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if int(self.board[(self.row_total-1-i)+gap][i][column_index])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Positive diagonal row and floor verification
        streak = 0
        gap = floor_index - column_index
        if column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if int(self.board[i+gap][row_index][i])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Negative diagonal row and floor verification
        streak = 0
        gap = floor_index - ((self.column_total-1)-column_index)
        if (self.column_total-1)-column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if int(self.board[(self.column_total-1-i)+gap][row_index][i])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Positive positive diagonal column, row and floor verification
        streak = 0
        gap = floor_index - row_index
        if row_index == column_index and row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if int(self.board[i+gap][i][i])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Positive negative diagonal column, row and floor verification
        streak = 0
        gap = floor_index - ((self.row_total-1)-row_index)
        if row_index == self.column_total-1-column_index and (self.row_total-1)-row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if int(self.board[(self.row_total-1-i)+gap][i][self.column_total-i-1])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Negative positive diagonal column, row and floor verification
        streak = 0
        gap = floor_index - column_index
        if row_index == self.column_total-1-column_index and column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if int(self.board[i+gap][i][self.column_total-i-1])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Negative negative diagonal column, row and floor verification
        streak = 0
        gap = floor_index - ((self.column_total-1)-column_index)
        if row_index == column_index and (self.column_total-1)-column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if int(self.board[(self.column_total-1-i)+gap][i][i])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        return False

    #def user_input_board(self):
    #    print("Enter the position (row and column, separated by space) and your usernumber : ")
    #    entries = list(map(int, input().split()))
    #    # Need to add this entrie to the UI
    #    return entries

    def graphic_representation(self):
        # not used for the moment

        x, y, z = np.indices((4, 4, 6))
        # link these parameters with add_piece definition
        robot_piece = (x == 3) & (y == 3) & (z == 0)
        user_piece = (x == 1) & (y == 2) & (z == 0)

        colors = np.empty(robot_piece.shape, dtype=object)
        colors[robot_piece] = 'blue'
        colors[user_piece] = 'red'

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.ax.voxels(robot_piece, facecolors=colors, edgecolor='k')
        self.ax.voxels(user_piece, facecolors=colors, edgecolor='k')
        self.ax.set_title("Connect 4 3D")
        self.ax.text2D(0, 0.94, "The robot plays the blue pieces\nYou play the red pieces", transform=self.ax.transAxes)
        
        # Add the FigureCanvas to the layout
        self.canvas = FigureCanvas(self.figure)
        self.setCentralWidget(self.canvas)
        return Figure
  

    def button_played(self):
        print("Button clicked, the player has played")

        #player, column, row = self.take_picture()
        #vision_list = [str(row), str(column), str(player)]
        #print('vision list : ', vision_list)
        #self.add_piece(vision_list)

        if self.push_button1.isChecked():
            user_input = self.line_edit1.text()
            entries = user_input.split()
            self.add_piece(entries)
            self.line_edit1.clear()
            self.push_button1.setChecked(False)
            
            win = self.detect_win(entries)
            if(win):
                print("VICTORY!")
#
        elif self.push_button2.isChecked():
            user_input = self.line_edit2.text()
            entries = user_input.split()
            self.add_piece(entries)
            self.line_edit2.clear()
            self.push_button2.setChecked(False)
            
            win = self.detect_win(entries)
            if(win):
                print("VICTORY!")
        
        self.label.setText(self.print_board())
        return #vision_list
        

    def take_picture(self):
        #global LastList
        start_time = time.time()
        list = self.LastList[:]

        # Create a VideoCapture object
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

        # Set the focus distance (try different values to see the effect)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        while list == self.LastList:
            i=0

            # Capture a frame from the webcam
            ret, img = cap.read()

            # Show the frame
            cv2.imshow("Webcam", img)

            # Exit the loop if the 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Crop the image and divise it into 16 squares
            center = (img.shape[1]//2, img.shape[0]//2)
            size = (1080, 1080)
            img = cv2.getRectSubPix(img, size, center)

            height, width, _ = img.shape
            square_size = (height//4, width//4)

            # Iterate through the rows and columns of the image
            for row in range(4):
                for col in range(4):
                    
                    # Extract each square of the image
                    square = img[row*square_size[0]:(row+1)*square_size[0], col*square_size[1]:(col+1)*square_size[1]]
                    gray_img = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)

                    # Detect QR codes
                    qr_codes = pyzbar.decode(gray_img)

                    # Add QR code to the list
                    for qr_code in qr_codes:
                        # Get QR code data
                        data = qr_code.data.decode()
                        list[i]=(int(data))                
                        #print(data)
                    i+=1
                    
            # Print the game board
            os.system('cls' if os.name == 'nt' else 'clear')
            for i in range(0, 16, 4):
                print(list[i:i+4])
            
            # Wait 0.2 seconds
            time.sleep(0.2)
        
        for i, (a, b) in enumerate(zip(list, self.LastList)):
            if a != b:
                x = i%4+1
                y = i//4+1
                if (a < 47):
                    Player = 'R'
                else:
                    Player = 'U'

        self.LastList = list
        print("--- %s seconds ---" % (time.time() - start_time))

        # Release the VideoCapture object and Close all the windows
        cap.release()
        cv2.destroyAllWindows()

        return Player, x, y
    
if __name__ == "__main__":
    #app = QApplication(sys.argv)
    app = QtWidgets.QApplication(sys.argv)
    window = gameboard()
    window.show()
    sys.exit(app.exec_())