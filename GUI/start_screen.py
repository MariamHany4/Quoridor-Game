from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from GUI.board_screen import BoardView
from Core.board import Board



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quoridor Game")
        self.setGeometry(700, 300, 900, 800)

        self.ai_player = QPushButton("AI Player")
        self.human_player = QPushButton("Human Player")

        self.UIinit()

 
        self.ai_player.clicked.connect(self.open_ai_mode)
        self.human_player.clicked.connect(self.open_human_mode)

    def UIinit(self):
        button_style = """
            QPushButton {
                background-color: #B57BF4;
                color: black;
                font-size: 22px;
                font-weight: bold;
                padding: 15px;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #A568E0;
            }
            QPushButton:pressed {
                background-color: #8A4DBC;
            }
        """

        self.ai_player.setStyleSheet(button_style)
        self.human_player.setStyleSheet(button_style)

        widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Select Player Mode")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 40px;
        """)

        layout.addWidget(title)
        layout.addWidget(self.ai_player)
        layout.addWidget(self.human_player)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(25)

        widget.setLayout(layout)
        self.setCentralWidget(widget)



    def open_ai_mode(self):
        self.board = BoardView("AI")  
        self.board.show()
        self.close()  

    def open_human_mode(self):
        self.board = BoardView("HUMAN")
        self.board.show()
        self.close()
