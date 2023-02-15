# Sandrine Gagne, February 1st 2023

import sys
import cv2
import pyzbar.pyzbar as pyzbar
import time
import os
try:
    from MotorControl import MotorMove
except:
    pass
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt

class gameboard(QtWidgets.QMainWindow):
    row_total = 4
    column_total = 4
    floor_total = 6
    board = []
    LastList = [0 for _ in range(16)]
    var = 0
    
    def __init__(self):
        # Function used to display the user interface (UI) and let the user use inputs to move the robot
        # to a certain position or tell the program he's done playing. 

        self.init_board()
        super().__init__()
        self.setWindowTitle("User Interface")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.label = QLabel("Gameboard")
        self.label.setText(self.print_board())
        self.label.setAlignment(Qt.AlignCenter)

        # Define elements of the UI ------------------------------------------------------------------------------------------
        self.push_button1 = QCheckBox("PLAYER 1\nClick me when you've played")
        self.push_button1.clicked.connect(self.player_played)
        self.line_edit1 = QLineEdit()

        self.push_button2 = QCheckBox("PLAYER 2\nClick me when you've played")
        #self.push_button2.clicked.connect(self.button_played)
        self.push_button2.clicked.connect(self.player_played)
        self.line_edit2 = QLineEdit()

        self.line_edit3 = QLineEdit("10")
        self.line_edit1_label = QLabel("X position :")
        self.line_edit1_label.setAlignment(Qt.AlignCenter)
        self.line_edit4 = QLineEdit("10")
        self.line_edit2_label = QLabel("Y position :")
        self.line_edit2_label.setAlignment(Qt.AlignCenter)
        self.line_edit5 = QLineEdit("10")
        self.line_edit3_label = QLabel("Z position :")
        self.line_edit3_label.setAlignment(Qt.AlignCenter)
        self.line_edit6 = QLineEdit("10")
        self.line_edit4_label = QLabel("J1 position :")
        self.line_edit4_label.setAlignment(Qt.AlignCenter)
        self.line_edit7 = QLineEdit("10")
        self.line_edit5_label = QLabel("J2 position :")
        self.line_edit5_label.setAlignment(Qt.AlignCenter)
        self.line_edit6_label = QLabel("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")               #top right display only

        self.submit_button1 = QPushButton("Submit x-y-z-coordinates")
        self.submit_button1.clicked.connect(self.submit_inputs_xyz)
        self.submit_button2 = QPushButton("Submit joints coordinates")
        self.submit_button2.clicked.connect(self.submit_inputs_joints)

        actXPos, actYPos, actZPos = self.actual_position_xyz()
        self.line_edit6_label = QLabel("Actual X position :" + str(actXPos))
        self.line_edit6_label.setAlignment(Qt.AlignCenter)
        self.line_edit7_label = QLabel("Actual Y position :" + str(actYPos))
        self.line_edit7_label.setAlignment(Qt.AlignCenter)
        self.line_edit8_label = QLabel("Actual Z position :" + str(actZPos))
        self.line_edit8_label.setAlignment(Qt.AlignCenter)
        
        actJ1Pos, actJ2Pos = self.actual_position_joints()
        self.line_edit9_label = QLabel("Actual J1 position :" + str(actJ1Pos))
        self.line_edit9_label.setAlignment(Qt.AlignCenter)
        self.line_edit10_label = QLabel("Actual J2 position :" + str(actJ2Pos))
        self.line_edit10_label.setAlignment(Qt.AlignCenter)
        self.line_edit12_label = QLabel("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n") 
        self.line_edit13_label = QLabel("\n")      

        # Position keyboard to go to a precise gameboard position -------------------------------------------------------------
        self.selected_btn = None
        self.selected_floor = None
        button_names = ["A1", "B1", "C1", "D1", "A2", "B2", "C2", "D2", 
                        "A3", "B3", "C3", "D3", "A4", "B4", "C4", "D4"]
        floor_names =  ["Floor1", "Floor2", "Floor3", "Floor4", "Floor5", "Floor6"]

        self.buttons = []
        for i in range(16):
            self.buttons.append(QPushButton(str(button_names[i])))
            self.buttons[i].clicked.connect(lambda checked, btn=self.buttons[i]: self.update_selected_btn(btn))
            self.grid_layout.addWidget(self.buttons[i], i//4, i%4)
        for j in range(6):
            self.buttons.append(QPushButton(str(floor_names[j])))
            self.buttons[16+j].clicked.connect(lambda checked, floor=self.buttons[16+j]: self.update_selected_floor(floor))
            self.grid_layout.addWidget(self.buttons[16+j])
        
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_gameboard_pos)
        self.grid_layout.addWidget(self.submit_button)
                
        # Display layouts ----------------------------------------------------------------------------------------------------
        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.push_button1)
        self.left_layout.addWidget(self.line_edit1)
        self.left_layout.addWidget(self.push_button2)
        self.left_layout.addWidget(self.line_edit2)

        self.top_right_layout = QVBoxLayout()
        self.top_right_layout.addWidget(self.line_edit1_label)
        self.top_right_layout.addWidget(self.line_edit3)
        self.top_right_layout.addWidget(self.line_edit2_label)
        self.top_right_layout.addWidget(self.line_edit4)
        self.top_right_layout.addWidget(self.line_edit3_label)
        self.top_right_layout.addWidget(self.line_edit5)
        self.top_right_layout.addWidget(self.submit_button1)
        self.top_right_layout.addWidget(self.line_edit4_label)
        self.top_right_layout.addWidget(self.line_edit6)
        self.top_right_layout.addWidget(self.line_edit5_label)
        self.top_right_layout.addWidget(self.line_edit7)
        self.top_right_layout.addWidget(self.submit_button2)
        self.top_right_layout.addWidget(self.line_edit12_label)
        
        self.new_right_layout = QVBoxLayout()
        self.new_right_layout.addWidget(self.line_edit6_label)
        self.new_right_layout.addWidget(self.line_edit7_label)
        self.new_right_layout.addWidget(self.line_edit8_label)
        self.new_right_layout.addWidget(self.line_edit13_label)
        self.new_right_layout.addWidget(self.line_edit9_label)
        self.new_right_layout.addWidget(self.line_edit10_label)
        self.new_right_layout.addWidget(self.line_edit12_label)
        self.new_right_layout.addWidget(self.line_edit13_label)
        
        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.top_right_layout)
        self.main_layout.addLayout(self.new_right_layout)
        self.main_layout.addLayout(self.grid_layout)
  
        self.central_widget.setLayout(self.main_layout)     
        return
    
 
    def init_board(self):
        # Uses the global variables to generate the gameboard matrix

        x = self.row_total
        y = self.column_total
        z = self.floor_total
        self.board = [[[0 for k in range(x)] for j in range(y)] for i in range(z)]
        return

    def print_board(self):
        # Generate a visual representation of the gameboard to see what the robot / program knows of the game status.

        i = 1
        usermatrix = ('')
        for row in self.board:
            stringmatrix = ("\n\n                         A  B  C  D    floor = " + str(i) + "\n\n" + "1    " + str(row[0]) + "\n" + "2    " + str(
                row[1]) + "\n" + "3    " + str(row[2]) + "\n" + "4    " + str(row[3]))
            usermatrix = usermatrix + stringmatrix
            i += 1
        return usermatrix

    def add_piece(self, position_list):
        # Display the piece played on the UI to refresh the gameboard.

        row = int(position_list[0])
        column = int(position_list[1])
        player_id = int(position_list[2])
        limit_board = self.row_or_column_limit(row, column)
        if limit_board == 1:
            floor = self.determine_floor(row, column)
            if floor != None and limit_board == 1:
                self.board[floor - 1][row - 1][column - 1] = player_id

        self.label.setText(self.print_board())
        if self.detect_win(position_list):
            self.label.setText("Player " + str(player_id) + " won!")
        return

    def delete_piece(self, row, column, floor):
        # Delete the piece played on the UI to refresh the gameboard.

        self.board[floor - 1][row - 1][column - 1] = 0
        return

    def row_or_column_limit(self, row, column):
        # Returns an error if the player is trying to play out of the gameboard range limit. 
        # Asks the player to play at another position. 

        row = int(row)
        column = int(column)
        if row > 4 or column > 4:
            print('This case is not reachable. Try again.')
            self.add_piece(self.player_played())
            return 0
        return 1

    def determine_floor(self, row, column):
        # Calculate the actual floor of the piece, knowing the previous pieces played at this exact position. 

        floor = 1
        row = int(row)
        column = int(column)
        for i in range(1, 7):
            if self.board[i - 1][row - 1][column - 1] != 0:
                floor = floor + 1   
        if floor > 6:
            print('This case is not reachable. Try again.')
            self.add_piece(self.player_played())
            return None
        #else:
            #print('floor value is : ', floor)               
        return floor

    def detect_win(self,position_list):
        
        row_index = int(position_list[0])-1
        column_index = int(position_list[1])-1
        player_id = int(position_list[2])
        floor_index = 0
        for i in range(self.floor_total):
                    if self.board[i][row_index][column_index] == 0:  
                        floor_index = i-1
                        break
        if i == self.floor_total-1:
            floor_index = i
            print("max floor reached")

        #Row verification
        streak = 0
        for i in range(0,self.row_total):
            if int(self.board[floor_index][i][column_index])==player_id:
                streak = streak + 1
                if streak == 4:
                    return True
            else:
                streak = 0
        #Column verification
        streak = 0
        for i in range(0,self.column_total):
            if int(self.board[floor_index][row_index][i])==player_id:
                streak = streak + 1
                if streak == 4:
                    return True
            else:
                streak = 0
        #Floor verification
        streak = 0
        for i in range(0,self.floor_total):
            if int(self.board[i][row_index][column_index])==player_id:
                streak = streak + 1
                if streak == 4:
                    return True
            else:
                streak = 0
        #Positive diagonal column and row verification
        streak = 0
        if row_index == column_index:
            for i in range(0,self.column_total):
                if int(self.board[floor_index][i][i])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Negative diagonal column and row verification
        streak = 0
        if row_index == self.column_total-1-column_index:
            for i in range(0,self.column_total):
                if int(self.board[floor_index][i][self.column_total-i-1])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Positive diagonal column and floor verification
        streak = 0
        gap = floor_index - row_index
        if row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if int(self.board[i+gap][i][column_index])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Negative diagonal column and floor verification
        streak = 0
        gap = floor_index - ((self.row_total-1)-row_index)
        if (self.row_total-1)-row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if int(self.board[(self.row_total-1-i)+gap][i][column_index])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Positive diagonal row and floor verification
        streak = 0
        gap = floor_index - column_index
        if column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if int(self.board[i+gap][row_index][i])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Negative diagonal row and floor verification
        streak = 0
        gap = floor_index - ((self.column_total-1)-column_index)
        if (self.column_total-1)-column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if int(self.board[(self.column_total-1-i)+gap][row_index][i])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Positive positive diagonal column, row and floor verification
        streak = 0
        gap = floor_index - row_index
        if row_index == column_index and row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if int(self.board[i+gap][i][i])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Positive negative diagonal column, row and floor verification
        streak = 0
        gap = floor_index - ((self.row_total-1)-row_index)
        if row_index == self.column_total-1-column_index and (self.row_total-1)-row_index <= floor_index and gap <= self.floor_total-self.row_total:
            for i in range(0,self.row_total):
                if int(self.board[(self.row_total-1-i)+gap][i][self.column_total-i-1])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Negative positive diagonal column, row and floor verification
        streak = 0
        gap = floor_index - column_index
        if row_index == self.column_total-1-column_index and column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if int(self.board[i+gap][i][self.column_total-i-1])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        #Negative negative diagonal column, row and floor verification
        streak = 0
        gap = floor_index - ((self.column_total-1)-column_index)
        if row_index == column_index and (self.column_total-1)-column_index <= floor_index and gap <= self.floor_total-self.column_total:
            for i in range(0,self.column_total):
                if int(self.board[(self.column_total-1-i)+gap][i][i])==player_id:
                    streak = streak + 1
                    if streak == 4:
                        return True
                else:
                    streak = 0
        return False

    #def user_input_board(self):
    #    print("Enter the position (row and column, separated by space) and your usernumber : ")
    #    entries = list(map(int, input().split()))
    #    # Need to add this entrie to the UI
    #    return entries

    def player_played(self):
        # Actualize the gameboard status with the new inputs
        print('HI')
        ##player, column, row = self.take_picture()
        ##vision_list = [str(row), str(column), str(player)]
        ##print('vision list : ', vision_list)
        ##self.add_piece(vision_list)

        if self.push_button1.isChecked():
            user_input = self.line_edit1.text()    # Uncomment thoses lines to use the player's input
            entries = user_input.split()           # Comment thoses lines to use the vision input
            self.add_piece(entries)                # " "  
            self.line_edit1.clear()                # " "
            self.push_button1.setChecked(False)
#
        elif self.push_button2.isChecked():
       #     user_input = self.line_edit2.text()
       #     entries = user_input.split()
       #     self.add_piece(entries)
       #     self.line_edit2.clear()
            self.push_button2.setChecked(False)
            
            win = self.detect_win(entries)
            if(win):
                print("VICTORY!")
        
        self.label.setText(self.print_board())
        return vision_list

    def submit_inputs_xyz(self):
        xPosition = self.line_edit3.text()
        yPosition = self.line_edit4.text()
        zPosition = self.line_edit5.text()
        # Link with Alex's code
        return xPosition, yPosition, zPosition

    def actual_position_xyz(self):
        # Link with Alex's code 
        xActual = 1
        yActual = 2
        zActual = 2
        return xActual, yActual, zActual

    def submit_inputs_joints(self):
        joint1Position = self.line_edit6.text()
        joint2Position = self.line_edit7.text()
        # Link with Alex's code
        return joint1Position, joint2Position

    def update_selected_btn(self, btn):
        self.selected_btn = btn

    def update_selected_floor(self, floor):
        self.selected_floor = floor

    def submit_gameboard_pos(self):
        if self.selected_btn and self.selected_floor:
            self.button_played(self.selected_btn, self.selected_floor)

    def button_played(self, btn, floor):
        gameboardPosition = [btn.text(), floor.text()]
        print("gameboardposition : ", gameboardPosition)
        return gameboardPosition

    def take_picture(self):
        # Take picture of the gameboard when the played button is press. Actualize the UI by comparing the actual status gameboard
        # and the previous status gameboard. 

        start_time = time.time()
        list = self.LastList[:]

        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)        # Create a VideoCapture object 
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)         # Set the focus distance
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)        # Set the focus distance

        while list == self.LastList:
            i=0
            ret, img = cap.read()                       # Capture a frame from the webcam
            cv2.imshow("Webcam", img)                   # Show the frame

            if cv2.waitKey(1) & 0xFF == ord('q'):       # Exit the loop if the 'q' key is pressed
                break

            center = (img.shape[1]//2, img.shape[0]//2) # Crop the image and divise it into 16 squares
            size = (1080, 1080)
            img = cv2.getRectSubPix(img, size, center)

            height, width, _ = img.shape
            square_size = (height//4, width//4)

            for row in range(4):                        # Iterate through the rows and columns of the image
                for col in range(4):
                    square = img[row*square_size[0]:(row+1)*square_size[0], col*square_size[1]:(col+1)*square_size[1]]  # Extract each square of the image
                    gray_img = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)
                    
                    qr_codes = pyzbar.decode(gray_img)  # Detect QR codes
                    for qr_code in qr_codes:            # Add QR code to the list
                        data = qr_code.data.decode()    # Get QR code data
                        list[i]=(int(data))                
                    i+=1
                    
            os.system('cls' if os.name == 'nt' else 'clear')    # Print the game board
            for i in range(0, 16, 4):
                print(list[i:i+4])
            
            time.sleep(0.2)                             # Wait 0.2 seconds
        
        for i, (a, b) in enumerate(zip(list, self.LastList)):
            if a != b:
                x = i%4+1
                y = i//4+1
                if (a < 47):
                    Player = 'R'
                else:
                    Player = 'U'

        self.LastList = list
        #print("--- %s seconds ---" % (time.time() - start_time))
        cap.release()                                   # Release the VideoCapture object and Close all the windows
        cv2.destroyAllWindows()
        return Player, x, y
    
if __name__ == "__main__":
    #app = QApplication(sys.argv)
    gm = gameboard
    app = QtWidgets.QApplication(sys.argv)
    window = gameboard()
    window.show()
    sys.exit(app.exec_())