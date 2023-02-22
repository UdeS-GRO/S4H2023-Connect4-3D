# Jacob Lambert, January 17th 2023

from GameBoardRepresentation import gameboard
import random

import sys
from PyQt5 import QtWidgets

import os
from streak_counter import streak_counter

class AI():
    def __init__(self, gb):
        self.gb = gb
        self.board = gb.board
        self.row_total = gb.row_total
        self.column_total = gb.column_total
        self.floor_total = gb.floor_total
        self.AI_id = 1
        self.opponent_id = 2
        return
        
    def get_positions(self):
        possible_positions = []
        for i in range(self.gb.row_total):
            for j in range(self.gb.column_total):
                for k in range(self.gb.column_total):
                    if self.gb.board[i][j][k] == 0:  
                        possible_positions.append([i+1,j+1,k+1])
                        break
        return possible_positions

    def rate_play(self,play):
        strength=0
        streak_list = streak_counter(play,self.board,self.row_total,self.column_total,self.floor_total)
        for streak in streak_list:
            if streak == 1:
                strength=strength+11
            elif streak == 2:
                strength=strength+101
            elif streak == 3:
                strength=strength+1001
            elif streak == 4:
                strength=strength+10001
        opponent_play = [play[0],play[1],self.opponent_id]
        for streak in streak_counter(opponent_play,self.board,self.row_total,self.column_total,self.floor_total):
            if streak == 1:
                strength=strength+10
            elif streak == 2:
                strength=strength+100
            elif streak == 3:
                strength=strength+1000
            elif streak == 4:
                strength=strength+10000
    
        return strength

    def choose_play(self):
        possible_positions = self.get_positions()
        max_strength = 0
        best_plays = []
        rated_plays = []
        for position in possible_positions:
            play = [str(position[0])]+[str(position[1])]+[self.AI_id]
            strength = self.rate_play(play)
            rated_plays.append([play,strength])
            if strength > max_strength:
                max_strength = strength
                best_plays = [play]
            elif strength == max_strength:
                best_plays.append(play)
        best_play = random.choice(best_plays)

        return best_play

if __name__=="__main__":

    print("AI_algoritm.py is being run directly")
    app = QtWidgets.QApplication(sys.argv)
    gb = gameboard()
    gb.board
    AI = AI(gb)
    play = AI.choose_play()
    position_list = [play[0],play[1],'2']
    gb.add_piece(position_list)
    
    gb.show()
    sys.exit(app.exec_())


