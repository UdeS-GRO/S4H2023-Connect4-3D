from GameBoardRepresentation import gameboard
from AI_algoritm import AI

import sys
from PyQt5 import QtWidgets

import os

class main():
    def __init__(self,gb,AI):
        self.gb = gb
        self.AI = AI
        
    def AI_played(self):
        play = AI.choose_play()
        position_list = [str(play[0]),str(play[1]),'2']
        gb.add_piece(position_list)
        gb.line_edit2.clear()
        gb.push_button2.setChecked(False)
        if(gb.detect_win(play)):
                print("VICTORY!")
        gb.label.setText(gb.print_board())



if __name__=="__main__":
    os.system('cls')
    app = QtWidgets.QApplication(sys.argv)
    gb = gameboard()
    gb.board
    AI = AI(gb)
    main(gb,AI)
    gb.push_button2.clicked.connect(main.AI_played)
    gb.show()
    sys.exit(app.exec_())