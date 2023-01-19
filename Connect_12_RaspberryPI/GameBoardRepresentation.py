# Sandrine Gagne, January 12th 2023

import numpy as np
import matplotlib.pyplot as plt
from tkinter import *


class gameboard(object):
    row_total = 4
    column_total = 4
    floor_total = 6
    board = []

    def __init__(self):
        self.init_board()

    def init_board(self):
        x = self.row_total
        y = self.column_total
        z = self.floor_total
        self.board = [[[0 for k in range(x)] for j in range(y)] for i in range(z)]
        return

    def print_board(self):
        i = 0
        root = Tk()
        root.title('Game Board Matrix')
        root.geometry("200x800")
        label0 = Label(root, text="Game Board ID's and positions")
        label0.pack()
        for row in self.board:
            print("____________________________")
            label1 = Label(root, text="____________________________")
            print("      A  B  C  D    floor = " + str(i) + "\n\n" + "1    " + str(row[0]) + "\n" + "2    " + str(
                row[1]) + "\n" + "3    " + str(row[2]) + "\n" + "4    " + str(row[3]))
            label2 = Label(root, text="      A  B  C  D    floor = " + str(i) + "\n\n" + "1    " + str(
                row[0]) + "\n" + "2    " + str(
                row[1]) + "\n" + "3    " + str(row[2]) + "\n" + "4    " + str(row[3]))
            i += 1
            label1.pack()
            label2.pack()
        print("____________________________")
        label3 = Label(root, text="____________________________")
        label3.pack()
        # Put the button in another function and register the input to use it
        played_button = Button(root, text="Played").place(x=70, y=750)
        return

    def add_piece(self, row, column, floor, id):
        self.board[floor - 1][row - 1][column - 1] = id
        return

    def delete_piece(self, row, column, floor):
        self.board[floor - 1][row - 1][column - 1] = 0
        return

    def user_input_board(self):
        # use for debug instead of add_piece
        R = int(input("Enter the number of rows: "))
        C = int(input("Enter the number of columns: "))
        F = int(input("Enter the number of floors: "))

        print("Enter the entries in a single line (separated by space): ")
        entries = list(map(int, input().split()))
        matrix = np.array(entries).reshape(R, C, F)
        print(matrix)

    def graphic_representation(self):
        x, y, z = np.indices((4, 4, 6))
        # link these parameters with add_piece definition
        robot_piece = (x == 3) & (y == 3) & (z == 0)
        user_piece = (x == 1) & (y == 2) & (z == 0)

        colors = np.empty(robot_piece.shape, dtype=object)
        colors[robot_piece] = 'blue'
        colors[user_piece] = 'red'

        ax = plt.figure().add_subplot(projection='3d')
        ax.voxels(robot_piece, facecolors=colors, edgecolor='k')
        ax.voxels(user_piece, facecolors=colors, edgecolor='k')
        ax.set_title("Connect 4 3D")
        ax.text2D(0, 0.94, "The robot plays the blue pieces\nYou play the red pieces", transform=ax.transAxes)
        plt.show()
        return

if __name__=="__main__":
    gm = gameboard()
    
    gm.add_piece(1, 1, 1, 1)
    gm.add_piece(2, 2, 1, 2)
    gm.add_piece(3, 3, 1, 3)
    gm.add_piece(4, 4, 1, 4)
    gm.add_piece(1, 1, 2, 5)
    gm.add_piece(2, 2, 2, 6)
    gm.add_piece(3, 3, 2, 7)
    gm.add_piece(4, 4, 2, 8)
    gm.delete_piece(3, 3, 1)
    gm.print_board()
    
    gm.graphic_representation()
