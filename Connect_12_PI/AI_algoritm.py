# Jacob Lambert, January 17th 2023

from GameBoardRepresentation import gameboard
from GameBoardRepresentation import gamewindow

import sys
import numpy as np
from tkinter import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit
from PyQt5.QtCore import Qt

import cv2
import numpy as np
import pyzbar
import time
import os

class AI():

    def __init__(self, gb):
        self.gb = gb
        self.board = gb.board
        self.row_total = gb.row_total
        self.column_total = gb.column_total
        self.floor_total = gb.floor_total
        return
        
    def get_plays(self):
        possible_plays = []
        for i in range(self.gb.row_total):
            for j in range(self.gb.column_total):
                for k in range(self.gb.column_total):
                    if self.gb.board[i][j][k] == 0:  
                        possible_plays.append([i+1,j+1,k+1])
                        break
        return possible_plays

    def rate_play(self,play):
        strength = 0

        return strength
        
    """def detect_lines(self,play):
        row_index = play[0]-1
        column_index = play[0]-1
        floor_index = play[0]-1

        #Row lines
        streak = 0
        for i in range(0,self.row_total-1):
            if self.gb.board[i][column_index][floor_index]==self.gb.board[row_index][column_index][floor_index]:
                streak = streak +1

            elif self.gb.board[i][column_index][floor_index] != 0:
                streak = 0"""

    #def choose_play(self):

    def detect_win(self,play):
        
        row_index = int(play[1])-1
        column_index = int(play[0])-1
        floor_index = int(play[2])-1

        print(self.board[row_index][column_index][floor_index])

        #Row verification
        streak = 0
        for i in range(0,self.row_total):
            if self.board[i][column_index][floor_index]==self.board[row_index][column_index][floor_index]:
                streak = streak + 1
                if streak == 4:
                    return True
            else:
                streak = 0
        #Column verification
        streak = 0
        for i in range(0,self.column_total):
            if self.board[row_index][i][floor_index]==self.board[row_index][column_index][floor_index]:
                streak = streak + 1
                if streak == 4:
                    return True
            else:
                streak = 0
        #Positive diagonal column and row verification
        streak = 0
        for i in range(0,self.column_total):
            if row_index+i > self.row_total-1 or column_index+i > self.row_total-1:
                break
            if self.board[row_index+i][row_index+i][floor_index]==self.board[row_index][column_index][floor_index]:
                streak = streak + 1
                if streak == 4:
                        return True
            else:
                streak = 0
        #Negative diagonal column and row verification
        streak = 0
        for j in range(0,self.column_total-1):
            if row_index+j > self.row_total-1 or column_index+j > self.row_total-1:
                break
            if self.board[row_index-j][row_index+j][floor_index]==self.board[row_index][column_index][floor_index]:
                streak = streak + 1
                if streak == 4:
                        return True
            else:
                streak = 0
        return False

if __name__=="__main__":

    gb = gameboard()
    AI = AI(gb)
    play = ["1","1","1"]
    gb.add_piece(play)
    print(AI.detect_win(play))
    play = ["1","2","1"]
    gb.add_piece(play)
    print(AI.detect_win(play))
    play = ["1","3","1"]
    gb.add_piece(play)
    print(AI.detect_win(play))
    play = ["1","4","1"]
    gb.add_piece(play)
    print(AI.detect_win(play))
    

    #app = QtWidgets.QApplication(sys.argv)
    #window = gamewindow(gb)
    #window.show()
    #sys.exit(app.exec_())
 

