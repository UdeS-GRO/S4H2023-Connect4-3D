# Jacob Lambert, January 17th 2023

from GameBoardRepresentation import gameboard
import random

import sys
from PyQt5 import QtWidgets

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

    def choose_play(self):
        possible_plays = self.get_plays()
        best_play = random.choice(possible_plays)
        return best_play

if __name__=="__main__":

    print("AI_algoritm.py is being run directly")
    app = QtWidgets.QApplication(sys.argv)
    gb = gameboard()
    gb.board
    #AI = AI(gb)
    #app = QtWidgets.QApplication(sys.argv)
    #window = gamewindow(gb)
    #window.show()
    #sys.exit(app.exec_())
 

