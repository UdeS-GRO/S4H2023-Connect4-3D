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
        
    def streak_counter(self,play):
        
        streak_list = []
        row_index = int(play[0])-1
        column_index = int(play[1])-1
        
        for i in range(self.floor_total):
                    if self.board[i][row_index][column_index] == 0:  
                        floor_index = i-1
                        break

        #Row counter
        streak = 0
        for i in range(0,self.row_total):
            if int(self.board[floor_index][i][column_index])!=self.board[floor_index][row_index][column_index]:
                if int(self.board[floor_index][i][column_index])!=0:
                   streak_list
                   streak = 0
                else:
                    streak = streak + 1
        streak_list.append(streak)
                        
        #Column counter
        streak = 0
        for i in range(0,self.column_total):
            if int(self.board[floor_index][row_index][i])!=self.board[floor_index][row_index][column_index]:
                if int(self.board[floor_index][row_index][i])!=0:
                   streak_list.append(streak)
                   streak = 0
                else:
                    streak = streak + 1
        streak_list.append(streak)
                        
        #Floor counter
        streak = 0
        for i in range(0,self.floor_total):
            if int(self.board[i][row_index][column_index])!=self.board[floor_index][row_index][column_index]:
                if int(self.board[i][row_index][column_index])!=0:
                   streak_list.append(streak)
                   streak = 0
                else:
                    streak = streak + 1
        streak_list.append(streak)
                        
        #Positive diagonal column and row counter
        streak = 0
        if row_index == column_index:
            for i in range(0,self.column_total):
                if int(self.board[floor_index][i][i])!=self.board[floor_index][row_index][column_index]:
                    if int(self.board[floor_index][i][i])!=0:
                        streak_list.append(streak)
                        streak = 0
                    else:
                        streak = streak + 1
            streak_list.append(streak)
        #Negative diagonal column and row counter
        streak = 0
        if row_index == self.column_total-1-column_index:
            for i in range(0,self.column_total):
                if int(self.board[floor_index][i][self.column_total-i-1])!=self.board[floor_index][row_index][column_index]:
                    if int(self.board[floor_index][i][self.column_total-i-1])!=0:
                        streak_list.append
                        streak = 0
                    else:
                        streak = streak + 1
            streak_list.append(streak)
        #Positive diagonal column and floor counter
        streak = 0
        gap = floor_index - row_index
        if row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if int(self.board[i+gap][i][column_index])!=self.board[floor_index][row_index][column_index]:
                    if int(self.board[i+gap][i][column_index])!=0:
                        streak_list.append
                        streak = 0
                    else:
                        streak = streak + 1
            streak_list.append(streak)
        #Negative diagonal column and floor counter
        streak = 0
        gap = floor_index - ((self.row_total-1)-row_index)
        if (self.row_total-1)-row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if int(self.board[(self.row_total-1-i)+gap][i][column_index])!=self.board[floor_index][row_index][column_index]:
                    if int(self.board[(self.row_total-1-i)+gap][i][column_index])!=0:
                        streak_list.append
                        streak = 0
                    else:
                        streak = streak + 1
            streak_list.append(streak)
        #Positive diagonal row and floor counter
        streak = 0
        gap = floor_index - column_index
        if column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if int(self.board[i+gap][row_index][i])!=self.board[floor_index][row_index][column_index]:
                    if int(self.board[i+gap][row_index][i])!=0:
                        streak_list.append
                        streak = 0
                    else:
                        streak = streak + 1
            streak_list.append(streak)
        #Negative diagonal row and floor counter
        streak = 0
        gap = floor_index - ((self.column_total-1)-column_index)
        if (self.column_total-1)-column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if int(self.board[(self.column_total-1-i)+gap][row_index][i])!=self.board[floor_index][row_index][column_index]:
                    streak_list
                    streak = 0
                else:
                    streak = streak + 1
        streak_list.append(streak)
        #Positive positive diagonal column, row and floor counter
        streak = 0
        gap = floor_index - row_index
        if row_index == column_index and row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if int(self.board[i+gap][i][i])!=self.board[floor_index][row_index][column_index]:

                    streak_list
                    streak = 0
                else:
                    streak = streak + 1
        streak_list.append(streak)
        #Positive negative diagonal column, row and floor counter
        streak = 0
        gap = floor_index - ((self.row_total-1)-row_index)
        if row_index == self.column_total-1-column_index and (self.row_total-1)-row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if int(self.board[(self.row_total-1-i)+gap][i][self.column_total-i-1])!=self.board[floor_index][row_index][column_index]:

                    streak_list
                    streak = 0
                else:
                    streak = streak + 1
        streak_list.append(streak)
        #Negative positive diagonal column, row and floor counter
        streak = 0
        gap = floor_index - column_index
        if row_index == self.column_total-1-column_index and column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if int(self.board[i+gap][i][self.column_total-i-1])!=self.board[floor_index][row_index][column_index]:

                    streak_list
                    streak = 0
                else:
                    streak = streak + 1
        streak_list.append(streak)
        #Negative negative diagonal column, row and floor counter
        streak = 0
        gap = floor_index - ((self.column_total-1)-column_index)
        if row_index == column_index and (self.column_total-1)-column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if int(self.board[(self.column_total-1-i)+gap][i][i])!=self.board[floor_index][row_index][column_index]:
                    if int(self.board[(self.column_total-1-i)+gap][i][i])!=0:
                        streak_list
                        streak = 0
                else:
                    streak = streak + 1
        streak_list.append(streak)
        return streak_list

    def rate_play(self,play):
        strength = sum(self.streak_counter(play))
        return strength

    def choose_play(self):
        possible_plays = self.get_plays()
        max_strength = 0
        best_plays = []
        for plays in possible_plays:
            if self.rate_play(plays) > max_strength:
                max_strength = self.rate_play(plays)
                best_plays = [plays]
            elif self.rate_play(plays) == max_strength:
                best_plays.append(plays)
        best_play = random.choice(best_plays)
        return best_play

if __name__=="__main__":

    print("AI_algoritm.py is being run directly")
    app = QtWidgets.QApplication(sys.argv)
    gb = gameboard()
    gb.board
    AI = AI(gb)
    play = AI.choose_play()
    print(play)
    position_list = [play[0],play[1],'2']
    gb.add_piece(position_list)
    
    gb.show()
    sys.exit(app.exec_())
 

