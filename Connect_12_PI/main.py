from GameBoardRepresentation import gameboard
from AI_algoritm import AI

import sys
from PyQt5 import QtWidgets

import os
os.system('cls||clear') # this line clears the screen 'cls' = windows 'clear' = unix
# below is my main script

class main():
    def __init__(self,gb,AI):
        self.gb = gb
        self.AI = AI
        
      
    def AI_button(self):
        print("AI button pressed")
        play = AI.choose_play()
        position_list = [play[0],play[1],'2']
        gb.add_piece(position_list)
        gb.line_edit2.clear()
        gb.push_button2.setChecked(False)



if __name__=="__main__":

    print("AI_algoritm.py is being run directly")
    app = QtWidgets.QApplication(sys.argv)
    gb = gameboard()
    gb.board
    AI = AI(gb)
    main(gb,AI)
    gb.push_button2.clicked.connect(main.AI_button)
    gb.show()
    sys.exit(app.exec_())