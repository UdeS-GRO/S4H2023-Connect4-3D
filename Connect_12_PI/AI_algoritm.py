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
        self.AI_id = 2
        self.opponent_id = 1

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
        for streak in streak_counter(play,self.gb.board,self.gb.row_total,self.gb.column_total,self.gb.floor_total):
            if streak == 1:
                strength=strength+11
            elif streak == 2:
                strength=strength+101
            elif streak == 3:
                strength=strength+1001
            elif streak == 4:
                strength=strength+10001
        opponent_play = [play[0],play[1],self.opponent_id]
        for streak in streak_counter(opponent_play,self.gb.board,self.gb.row_total,self.gb.column_total,self.gb.floor_total):
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
        for position in possible_positions:
            play = [position[0]]+[position[1]]+[self.AI_id]
            strength = self.rate_play(play)
            if strength > max_strength:
                max_strength = strength
                best_plays = [play]
            elif strength == max_strength:
                best_plays.append(play)
        best_play = random.choice(best_plays)

        return best_play
 

