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

    # Display the stats of the robot
    self.label2 = QLabel("Robot stats")
    self.label2.setText(self.print_stats())
    self.label2.setFixedHeight(80)
    style_sheet = """
    QLabel {
        background-color: #555956;
        color: white;
        font: bold;
        font-size: 20px;
        border-radius: 10px;
        border: 2px solid #37474f;
        padding: 6px 12px;
        margin: 4px 2px;
    }
    """
    self.label2.setStyleSheet(style_sheet)

    # Define elements of the UI ------------------------------------------
    self.submit_button1 = QPushButton("Nouvelle partie\n\nStart new game")
    style_sheet2 = """
    QPushButton {
        background-color: #555956;
        color: white;
        font: bold;
        font-size: 20px;
        border-radius: 10px;
        border: 2px solid #37474f;
        padding: 6px 12px;
        margin: 4px 2px;
    }
    """
    self.submit_button1.setStyleSheet(style_sheet2)
    self.submit_button1.clicked.connect(self.start_new_game)

    self.submit_button2 = QPushButton("Réservoir 45 remplis\n\nPick 45 deg just fulled")
    self.submit_button2.setStyleSheet(style_sheet2)
    self.submit_button2.clicked.connect(self.resetPick45deg)
    self.submit_button3 = QPushButton("Réservoir 90 remplis\n\nPick 90 deg just fulled")
    self.submit_button3.setStyleSheet(style_sheet2)
    self.submit_button3.clicked.connect(self.resetPick90deg)

    self.submit_button4 = QPushButton("J'ai joué\n\nI've played")
    style_sheet3 = """
    QPushButton {
        background-color: #4caf50;
        color: white;
        font: bold;
        font-size: 20px;
        border-radius: 10px;
        border: 2px solid #37474f;
        padding: 6px 12px;
        margin: 4px 2px;
    }
    """
    self.submit_button4.setStyleSheet(style_sheet3)

    # Move the buttons down when pressed
    self.submit_button1.pressed.connect(self.move_button1_down)
    self.submit_button2.pressed.connect(self.move_button2_down)
    self.submit_button3.pressed.connect(self.move_button3_down)
    self.submit_button4.pressed.connect(self.move_button4_down)

    self.submit_button1.released.connect(self.move_button1_up)
    self.submit_button2.released.connect(self.move_button2_up)
    self.submit_button3.released.connect(self.move_button3_up)
    self.submit_button4.released.connect(self.move_button4_up)

    # Display layouts ----------------------------------------------------
    self.left_layout = QVBoxLayout()
    self.left_layout.addWidget(self.submit_button4)

    self.right_layout = QVBoxLayout()
    self.right_layout.addWidget(self.submit_button1)
    self.right_layout.addWidget(self.submit_button2)
    self.right_layout.addWidget(self.submit_button3)
    self.right_layout.addWidget(self.label2)

    self.main_layout = QHBoxLayout()
    self.main_layout.addLayout(self.left_layout)
    self.main_layout.addWidget(self.label)
    self.main_layout.addLayout(self.right_layout)
    self.main_layout.addLayout(self.grid_layout)

    self.central_widget.setLayout(self.main_layout)
    return
