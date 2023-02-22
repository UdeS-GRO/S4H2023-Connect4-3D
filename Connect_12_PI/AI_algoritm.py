# Jacob Lambert, January 17th 2023

from GameBoardRepresentation import gameboard
import random

import sys
from PyQt5 import QtWidgets

import os

class AI():
    def __init__(self, gb):
        self.gb = gb
        self.board = gb.board
        self.row_total = gb.row_total
        self.column_total = gb.column_total
        self.floor_total = gb.floor_total
        self.AI_id = 'R'
        self.opponent_id = 'U'
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
        
    def streak_counter(self,play):
        
        streak_list = []
        row_index = int(play[0])-1
        column_index = int(play[1])-1
        for i in range(self.floor_total):
                    if self.board[i][row_index][column_index] == 0:  
                        floor_index = i
                        break
        
        player_id = play[2]

        #Row counter
        streak = 0
        for i in range(0,self.row_total):
            if i == row_index:
                streak = streak + 1
            elif self.board[floor_index][i][column_index]==player_id:
                streak = streak + 1
            elif self.board[floor_index][i][column_index]!='0':
                   streak = 0
                   break
        streak_list.append(streak)
        #Column counter
        streak = 0
        for i in range(0,self.column_total):
            if i == column_index:
                streak = streak + 1
            elif self.board[floor_index][row_index][i]==player_id:
                streak = streak + 1
            elif self.board[floor_index][row_index][i]!='0':
                   streak = 0
                   break
        streak_list.append(streak)                     
        #Floor counter
        streak = 0
        for i in range(0,self.floor_total):
            if i == floor_index:
                streak = streak + 1
            elif self.board[i][row_index][column_index]==player_id:
                streak = streak + 1
            elif self.board[i][row_index][column_index]!='0':
                   streak = 0
                   break
        streak_list.append(streak)              
        #Positive diagonal column and row counter
        streak = 0
        if row_index == column_index:
            for i in range(0,self.column_total):
                if i == column_index:
                    streak = streak + 1
                elif self.board[floor_index][i][i]==player_id:
                    streak = streak + 1
                elif self.board[floor_index][i][i]!='0':
                    streak = 0
                    break
            streak_list.append(streak)
        #Negative diagonal column and row counter
        streak = 0
        if (self.row_total-1)-row_index == column_index:
            for i in range(0,self.column_total):
                if i == column_index:
                    streak = streak + 1
                elif self.board[floor_index][(self.row_total-1-i)][i]==player_id:
                    streak = streak + 1
                elif self.board[floor_index][(self.row_total-1-i)][i]!='0':
                    streak = 0
                    break
            streak_list.append(streak)
        #Positive diagonal column and floor counter
        streak = 0
        gap = floor_index - row_index
        if row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if i == row_index:
                    streak = streak + 1
                elif self.board[i+gap][i][column_index]==player_id:
                    streak = streak + 1
                elif self.board[i+gap][i][column_index]!='0':
                        streak = 0
                        break
            streak_list.append(streak)
        #Negative diagonal column and floor counter
        streak = 0
        gap = floor_index - ((self.row_total-1)-row_index)
        if (self.row_total-1)-row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if i == row_index:
                    streak = streak + 1
                elif self.board[(self.row_total-1-i)+gap][i][column_index]==player_id:
                    streak = streak + 1
                elif self.board[(self.row_total-1-i)+gap][i][column_index]!='0':
                        streak = 0
                        break
            streak_list.append(streak)
        #Positive diagonal row and floor counter
        streak = 0
        gap = floor_index - column_index
        if column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if i == column_index:
                    streak = streak + 1
                elif self.board[i+gap][row_index][i]==player_id:
                    streak = streak + 1
                elif self.board[i+gap][row_index][i]!='0':
                        streak = 0
                        break
            streak_list.append(streak)
        #Negative diagonal row and floor counter
        streak = 0
        gap = floor_index - ((self.column_total-1)-column_index)
        if (self.column_total-1)-column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if i == column_index:
                    streak = streak + 1
                elif self.board[(self.column_total-1-i)+gap][row_index][i]==player_id:
                    streak = streak + 1
                elif self.board[(self.column_total-1-i)+gap][row_index][i]!='0':
                        streak = 0
                        break
            streak_list.append(streak)
        #Positive positive diagonal column, row and floor counter
        streak = 0
        gap = floor_index - row_index
        if row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if i == row_index:
                    streak = streak + 1
                elif self.board[i+gap][i][i]==player_id:
                    streak = streak + 1
                elif self.board[i+gap][i][i]!='0':
                        streak = 0
                        break
            streak_list.append(streak)
        #Positive negative diagonal column, row and floor counter
        streak = 0
        gap = floor_index - ((self.row_total-1)-row_index)
        if (self.row_total-1)-row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if i == row_index:
                    streak = streak + 1
                elif self.board[(self.row_total-1-i)+gap][i][i]==player_id:
                    streak = streak + 1
                elif self.board[(self.row_total-1-i)+gap][i][i]!='0':
                        streak = 0
                        break
            streak_list.append(streak)
        #Negative positive diagonal column, row and floor counter
        streak = 0
        gap = floor_index - column_index
        if column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if i == column_index:
                    streak = streak + 1
                elif self.board[i+gap][i][i]==player_id:
                    streak = streak + 1
                elif self.board[i+gap][i][i]!='0':
                        streak = 0
                        break
            streak_list.append(streak)
        #Negative negative diagonal column, row and floor counter
        streak = 0
        gap = floor_index - ((self.column_total-1)-column_index)
        if (self.column_total-1)-column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if i == column_index:
                    streak = streak + 1
                elif self.board[(self.column_total-1-i)+gap][i][i]==player_id:
                    streak = streak + 1
                elif self.board[(self.column_total-1-i)+gap][i][i]!='0':
                        streak = 0
                        break
            streak_list.append(streak)
        
        return streak_list

    def rate_play(self,play):
        strength=0
        for streak in self.streak_counter(play):
            if streak == 1:
                strength=strength+11
            elif streak == 2:
                strength=strength+101
            elif streak == 3:
                strength=strength+1001
            elif streak == 4:
                strength=strength+10001
        opponent_play = [play[0],play[1],self.opponent_id]
        for streak in self.streak_counter(opponent_play):
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
 

