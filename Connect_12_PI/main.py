from GameBoardRepresentation import gameboard
from AI_algoritm import AI
import sys
from PyQt5 import QtWidgets
import os
from MotorControl import MotorMove


def AI_played(self):
    play = AI.choose_play()
    print(play)
    print("AI")
    if (gb.detect_win(play)):
        MotorMove.sendVictory(MotorMove, 2)
        print("VICTORY! AI")
        gb.StatsAddWin(2)
    entries = [str(play[0]), str(play[1]), play[3]]
    gb.add_piece(entries)
    gb.submit_robot_pos(int(play[0]), int(play[1]), int(play[2]))
    gb.label.setText(gb.print_board())
    gb.take_picture()


def player_played(self):
    # Actualize the gameboard status with the new inputs
    player, column, row = gb.take_picture()
    entries = [str(row), str(column), str(player)]
    print("Player")
    if (gb.detect_win(entries)):
        MotorMove.sendVictory(MotorMove, 1)
        print("VICTORY! Human")
        gb.StatsAddWin(1)
    gb.add_piece(entries)
    AI_played(self)
    gb.label.setText(gb.print_board())

    return


if __name__ == "__main__":

    os.system('cls')
    app = QtWidgets.QApplication(sys.argv)
    gb = gameboard()
    gb.board
    AI = AI(gb)
    gb.submit_button4.clicked.connect(player_played)
    gb.show()
    sys.exit(app.exec_())
