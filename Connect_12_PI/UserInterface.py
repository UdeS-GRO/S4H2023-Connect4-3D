from PyQt5.QtWidgets import QGridLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt

def userInterface(self):
    # Generate the user interface
    self.setWindowTitle("User Interface")
    self.setGeometry(200, 200, 900, 500)    
    self.central_widget = QWidget()
    self.setCentralWidget(self.central_widget)
    self.grid_layout = QGridLayout()

    # Display the gameboard ---------------------------------------------
    self.label = QLabel("Gameboard")
    self.label.setText(self.print_board())
    self.label.setAlignment(Qt.AlignCenter) 
    
    # Define elements of the UI ------------------------------------------
    self.submit_button1 = QPushButton("Start new game")
    self.submit_button1.clicked.connect(self.start_new_game)
    self.submit_button2 = QPushButton("Pick 45 deg just fulled")
    self.submit_button2.clicked.connect(self.resetPick45deg)
    self.submit_button3 = QPushButton("Pick 90 deg just fulled")
    self.submit_button3.clicked.connect(self.resetPick90deg)

    self.submit_button4 = QPushButton("I've played")
    #self.submit_button4.clicked.connect(player_played)  

    # Display layouts ----------------------------------------------------
    self.left_layout = QVBoxLayout()
    self.left_layout.addWidget(self.submit_button4)
    
    self.right_layout = QVBoxLayout()
    self.right_layout.addWidget(self.submit_button1)
    self.right_layout.addWidget(self.submit_button2)
    self.right_layout.addWidget(self.submit_button3)

    self.main_layout = QHBoxLayout()
    self.main_layout.addLayout(self.left_layout)
    self.main_layout.addWidget(self.label)
    self.main_layout.addLayout(self.right_layout)
    self.main_layout.addLayout(self.grid_layout)

    self.central_widget.setLayout(self.main_layout)     
    return