from GameBoardRepresentation import gameboard
from AI_algoritm import AI

import sys
from PyQt5 import QtWidgets
import os

def AI_played(self):
    play = AI.choose_play()
    print(play)
    position_list = [str(play[0]),str(play[1]),AI.AI_id]
    #gb.submit_robot_pos(play[0],play[1],play[2])
    gb.add_piece(position_list)
    if(gb.detect_win(play)):
            print("VICTORY!")
    gb.label.setText(gb.print_board())

def player_played(self):
        # Actualize the gameboard status with the new inputs
        player, column, row = gb.take_picture()
        entries = [str(row), str(column), str(player)]
        print('vision list : ', entries)
        gb.add_piece(entries)

        if gb.push_button1.isChecked():
            #user_input = self.line_edit1.text()    # Uncomment thoses lines to use the player's input
            #entries = user_input.split()           # Comment thoses lines to use the vision input
            #self.add_piece(entries)                # " "  
            #self.line_edit1.clear()                # " "
            gb.push_button1.setChecked(False)
        if(gb.detect_win(entries)):
                print("VICTORY!")
                #close camera
                gb.cap.release()                                   # Release the VideoCapture object and Close all the windows
        gb.label.setText(gb.print_board())
        AI_played(self)
        
        return 

if __name__=="__main__":
    os.system('cls')
    app = QtWidgets.QApplication(sys.argv)
    gb = gameboard()
    gb.board
    AI = AI(gb)
    gb.push_button1.clicked.connect(player_played)
    gb.show()
    sys.exit(app.exec_())