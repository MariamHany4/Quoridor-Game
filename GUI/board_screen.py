from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Core.board import Board

class BoardView(QWidget):
    GRID_SIZE = 9  

    def __init__(self, mode):
        super().__init__()
        self.mode = mode
        self.setWindowTitle("Quoridor - Game Board")
        self.setGeometry(600, 200, 900, 850)

        self.cells = {}
        self.board_created = Board(self.mode == 'AI')
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()
        board_container = QVBoxLayout()

        title = QLabel(f"Quoridor - {self.mode} Mode")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            color: #4A148C;
            margin-bottom: 20px;
        """)
        board_container.addWidget(title)

        # GRID
        grid_widget = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        cell_style = """
            QPushButton {
                background-color: #EDE7F6;
                border: 2px solid #B39DDB;
                border-radius: 8px;
                min-width: 55px;
                min-height: 55px;
            }
            QPushButton:hover {
                background-color: #D1C4E9;
            }
        """

        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                btn = QPushButton("")
                btn.setStyleSheet(cell_style)
                btn.setProperty("row", r)
                btn.setProperty("col", c)
                btn.clicked.connect(self.handleCellClick)

                self.cells[(r, c)] = btn
                grid_layout.addWidget(btn, r, c)

        grid_widget.setLayout(grid_layout)
        board_container.addWidget(grid_widget)

    
        p1_row, p1_col = self.board_created.pawns["P1"]
        p2_row, p2_col = self.board_created.pawns["P2"]

        self.placePawn(p1_row, p1_col, "#4A148C")   
        self.placePawn(p2_row, p2_col, "#8254C2")   

   
        side_panel = QVBoxLayout()
        side_panel.setAlignment(Qt.AlignTop)

        self.label_turn = QLabel(f"Current Turn: {self.board_created.current_player}")
        self.label_turn.setStyleSheet("font-size: 22px; font-weight: bold; color: #4A148C;")
        side_panel.addWidget(self.label_turn)

        reset_btn = QPushButton("Restart Game")
        reset_btn.setStyleSheet("""
            background-color: #7E57C2;
            color: white;
            padding: 12px;
            border-radius: 12px;
            font-size: 18px;
        """)
        reset_btn.clicked.connect(self.resetGame)

        back_btn = QPushButton("Back to Menu")
        back_btn.setStyleSheet("""
            background-color: #9575CD;
            color: white;
            padding: 12px;
            border-radius: 12px;
            font-size: 18px;
        """)

        side_panel.addSpacing(40)
        side_panel.addWidget(reset_btn)
        side_panel.addWidget(back_btn)

        main_layout.addLayout(board_container, stretch=4)
        main_layout.addLayout(side_panel, stretch=1)
        self.setLayout(main_layout)


    def handleCellClick(self):
        btn = self.sender()
        r = btn.property("row")
        c = btn.property("col")
        print(f"Clicked cell: ({r}, {c})")

        current_player = self.board_created.current_player

        pawn_color = "#4A148C" if current_player == "P1" else "#8254C2"
        old_r, old_c = self.board_created.pawns[current_player]
        moved = self.board_created.move_pawn(current_player, (r, c))

        if moved:
            self.clearCell(old_r, old_c)
            self.placePawn(r, c, pawn_color)

            print("Pawn moved successfully.")
            self.label_turn.setText(f"Current Turn: {self.board_created.current_player}")

        else:
            print("Invalid move!")

    def clearCell(self, row, col):
        btn = self.cells[(row, col)]
        btn.setStyleSheet("""
            QPushButton {
                background-color: #EDE7F6;
                border: 2px solid #B39DDB;
                border-radius: 8px;
                min-width: 55px;
                min-height: 55px;
            }
        """)


    def placePawn(self, row, col, color="#4A148C"):
        btn = self.cells[(row, col)]
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 27px;
                border: 3px solid white;
                min-width: 55px;
                min-height: 55px;
            }}
        """)

    def resetGame(self):
        print("Game reset triggered")

        for (r, c), btn in self.cells.items():
            self.clearCell(r, c)

        self.label_turn.setText("Current Turn: Player 1")
