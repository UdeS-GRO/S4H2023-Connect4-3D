from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QCheckBox
from PyQt5.QtCore import Qt

def userInterface(self):
    self.setWindowTitle("User Interface")
    self.setGeometry(200, 200, 900, 500)    
    self.central_widget = QWidget()
    self.setCentralWidget(self.central_widget)
    self.grid_layout = QGridLayout()

    self.label = QLabel("Gameboard")
    self.label.setText(self.print_board())
    self.label.setAlignment(Qt.AlignCenter) 
    
    # Define elements of the UI ------------------------------------------------------------------------------------------
    self.push_button1 = QCheckBox("PLAYER 1\nClick me when you've played")
    self.push_button1.clicked.connect(self.player_played)
    self.line_edit1 = QLineEdit()   
    self.push_button2 = QCheckBox("PLAYER 2\nClick me when you've played")
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
    
    # create the toggle button
    self.toggle_button = QCheckBox("Manual Mode")
    self.toggle_button.setChecked(False)

    # create the other buttons
    self.toggle_button.toggled.connect(self.on_toggled) 
    self.submit_button1 = QPushButton("Submit x-y-z-coordinates")
    self.submit_button1.clicked.connect(self.submit_inputs_xyz)
    self.submit_button2 = QPushButton("Submit joints coordinates")
    self.submit_button2.clicked.connect(self.submit_inputs_joints)
    self.submit_button3 = QPushButton("Start automatic sequence")
    self.submit_button3.clicked.connect(self.submit_auto_startSequence)
    self.submit_button4 = QPushButton("Reset automatic sequence")
    self.submit_button4.clicked.connect(self.submit_auto_resetSequence)
    self.submit_button5 = QPushButton("Go to home")
    self.submit_button5.clicked.connect(self.submit_man_goToHome)
    self.submit_button6 = QPushButton("Go to pick 45 deg")
    self.submit_button6.clicked.connect(self.submit_man_goToPick45deg)
    self.submit_button7 = QPushButton("Go to pick 0 deg")
    self.submit_button7.clicked.connect(self.submit_man_goToPick0deg)
    self.submit_button8 = QPushButton("Go down")
    self.submit_button8.clicked.connect(self.submit_man_goDown)
    self.submit_button9 = QPushButton("Go to limit switch")
    self.submit_button9.clicked.connect(self.submit_man_goToLS)
    self.submit_button10 = QPushButton("Active electromagnet")
    self.submit_button10.clicked.connect(self.submit_man_grip)
    self.submit_button11 = QPushButton("Disable electromagnet")
    self.submit_button11.clicked.connect(self.submit_man_drop)  
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
    self.line_edit12_label = QLabel("\n")       
    
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

    self.submit_button = QPushButton("Go to place")
    self.submit_button.clicked.connect(self.submit_gameboard_pos)

    self.line_edit11_label = QLabel("Select a position,\na floor and  \n'Go to place'")
    self.grid_layout.addWidget(self.line_edit11_label)

    # Display layouts ----------------------------------------------------------------------------------------------------
    self.left_layout = QVBoxLayout()
    self.left_layout.addWidget(self.push_button1)
    self.left_layout.addWidget(self.line_edit1)
    self.left_layout.addWidget(self.push_button2)
    self.left_layout.addWidget(self.line_edit2) 

    self.top_right_layout = QVBoxLayout()
    self.top_right_layout.addWidget(self.toggle_button)
    self.top_right_layout.addWidget(self.submit_button3)
    self.top_right_layout.addWidget(self.submit_button4)
    self.top_right_layout.addWidget(self.submit_button5)
    self.top_right_layout.addWidget(self.submit_button6)
    self.top_right_layout.addWidget(self.submit_button7)
    self.top_right_layout.addWidget(self.submit_button)
    self.top_right_layout.addWidget(self.submit_button8)
    self.top_right_layout.addWidget(self.submit_button9)
    self.top_right_layout.addWidget(self.submit_button10)
    self.top_right_layout.addWidget(self.submit_button11)  
     
    self.new_right_layout = QVBoxLayout()
    self.new_right_layout.addWidget(self.line_edit1_label)
    self.new_right_layout.addWidget(self.line_edit3)
    self.new_right_layout.addWidget(self.line_edit2_label)
    self.new_right_layout.addWidget(self.line_edit4)
    self.new_right_layout.addWidget(self.line_edit3_label)
    self.new_right_layout.addWidget(self.line_edit5)
    self.new_right_layout.addWidget(self.submit_button1)
    self.new_right_layout.addWidget(self.line_edit4_label)
    self.new_right_layout.addWidget(self.line_edit6)
    self.new_right_layout.addWidget(self.line_edit5_label)
    self.new_right_layout.addWidget(self.line_edit7)
    self.new_right_layout.addWidget(self.submit_button2)
    self.new_right_layout.addWidget(self.line_edit6_label)
    self.new_right_layout.addWidget(self.line_edit7_label)
    self.new_right_layout.addWidget(self.line_edit8_label)
    self.new_right_layout.addWidget(self.line_edit9_label)
    self.new_right_layout.addWidget(self.line_edit10_label)
    self.new_right_layout.addWidget(self.line_edit12_label)

    self.main_layout = QHBoxLayout()
    self.main_layout.addLayout(self.left_layout)
    self.main_layout.addWidget(self.label)
    self.main_layout.addLayout(self.top_right_layout)
    self.main_layout.addLayout(self.new_right_layout)
    self.main_layout.addLayout(self.grid_layout)

    self.central_widget.setLayout(self.main_layout)     
    return