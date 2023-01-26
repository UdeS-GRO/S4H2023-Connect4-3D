# Sandrine Gagne, January 19th 2023

import sys
import numpy as np
from tkinter import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt


class gameboard(QtWidgets.QMainWindow):
    row_total = 4
    column_total = 4
    floor_total = 6
    board = []
        
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

        self.push_button = QPushButton("Click me when you've played")
        self.push_button.clicked.connect(self.button_played)

        #self.graphic_representation()
        #self.canvas = FigureCanvas(self.figure)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.push_button)
        #self.main_layout.addWidget(self.canvas)
        self.central_widget.setLayout(self.main_layout)
    
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
        row = position_list[0]
        column = position_list[1]
        player_id = position_list[2]
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
        if row > 4 or column > 4:
            print('This case is not reachable. Try again.')
            self.add_piece(self.user_input_board())
            return 0
        return 1

    def determine_floor(self, row, column):
        floor = 1
        for i in range(1, 7):
            if self.board[i - 1][row - 1][column - 1] != 0:
                floor = floor + 1   
        if floor > 6:
            print('This case is not reachable. Try again.')
            self.add_piece(self.user_input_board())
            return None
        else:
            print('floor value is : ', floor)               
        return floor

    def user_input_board(self):
        print("Enter the position (row and column, separated by space) and your usernumber : ")
        entries = list(map(int, input().split()))
        # Need to add this entrie to the UI
        return entries

    def graphic_representation(self):
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
        self.label.setAlignment(Qt.AlignCenter)
        self.push_button = QPushButton("Click me when you've played")
        self.push_button.clicked.connect(self.button_played)
        print("Button clicked, the player has played")
        # Needs to notify the robot that it's is turn
        return    
    
if __name__ == "__main__":
    #app = QApplication(sys.argv)
    app = QtWidgets.QApplication(sys.argv)
    window = gameboard()
    window.show()
    sys.exit(app.exec_())

gm = gameboard()
#gm.print_board()
#print('User 1, play!')
#gm.add_piece(gm.user_input_board())
#gm.print_board()
#print('User 2, play!')
#gm.add_piece(gm.user_input_board())
#gm.print_board()
