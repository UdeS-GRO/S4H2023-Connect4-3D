from GameBoardRepresentation import gameboard
from AI_algoritm import AI

import sys
from PyQt5 import QtWidgets
import os
from MotorControl import MotorMove
def AI_played(self):
    play = AI.choose_play()
<<<<<<< HEAD
    print(play)
    position_list = [str(play[0]),str(play[1]),AI.AI_id]
    if(gb.detect_win(play)):
            MotorMove.mssg7 = "2"
            print("VICTORY!")
    gb.submit_robot_pos(int(play[0]),int(play[1]),int(play[2]))
    gb.add_piece(position_list)
=======
    entries = [str(play[0]),str(play[1]),play[3]]
    gb.submit_robot_pos(int(play[0]),int(play[1]),int(play[2]))
    if(gb.detect_win(entries)):
            print("VICTORY! Robot")
    gb.add_piece(entries)
>>>>>>> 78583e1ddf996da572fc083b5f52570d821ae64d
    gb.label.setText(gb.print_board())
    gb.take_picture()



def player_played(self):
        # Actualize the gameboard status with the new inputs
        player, column, row = gb.take_picture()
        entries = [str(row), str(column), str(player)]
        if gb.push_button1.isChecked():
            #user_input = self.line_edit1.text()    # Uncomment thoses lines to use the player's input
            #entries = user_input.split()           # Comment thoses lines to use the vision input
            #self.add_piece(entries)                # " "  
            #self.line_edit1.clear()                # " "
            gb.push_button1.setChecked(False)
        if(gb.detect_win(entries)):
<<<<<<< HEAD
                MotorMove.mssg7 = "1"
                print("VICTORY!")
=======
                print("VICTORY! Player")
>>>>>>> 78583e1ddf996da572fc083b5f52570d821ae64d
                gb.cap.release()                                   # Release the VideoCapture object and Close all the windows
        gb.add_piece(entries)
        AI_played(self)
        gb.label.setText(gb.print_board())
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