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
        self.setGeometry(600, 200, 950, 900)

        self.cells = {}
        self.board_created = Board(self.mode == 'AI')
        self.initUI()

    def initUI(self):

        main_layout = QHBoxLayout()
        board_container = QVBoxLayout()

        # ▣ Background: Beige → Wood Tan Gradient
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #F4E8D3, stop:1 #D2B48C
                );
            }
        """)

        # ▣ Title styled with dark wood
        title = QLabel(f"Quoridor - {self.mode} Mode")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 34px;
            font-weight: 900;
            color: #4E2A1E;   /* Dark Walnut */
            padding: 15px;
            border-radius: 12px;
            background-color: rgba(255, 248, 230, 0.75);
            margin-bottom: 25px;
        """)
        board_container.addWidget(title)

        # ▣ Board grid with wooden tiles
        grid_widget = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        tile_style = """
            QPushButton {
                background-color: #F2DFC2;     /* Light Wood */
                border: 2px solid #B79267;      /* Mid-Wood Border */
                border-radius: 12px;
                min-width: 65px;
                min-height: 65px;
                box-shadow: 2px 2px 6px rgba(0,0,0,0.25);
            }
            QPushButton:hover {
                background-color: #E8D4B8;
                border: 2px solid #A67C52;
            }
        """

        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                btn = QPushButton("")
                btn.setStyleSheet(tile_style)
                btn.setProperty("row", r)
                btn.setProperty("col", c)
                btn.clicked.connect(self.handleCellClick)

                self.cells[(r, c)] = btn
                grid_layout.addWidget(btn, r, c)

        grid_widget.setLayout(grid_layout)
        board_container.addWidget(grid_widget)

        # ▣ Player spawn (pawns)
        p1_r, p1_c = self.board_created.pawns["P1"]
        p2_r, p2_c = self.board_created.pawns["P2"]

        # Pawns match the wood theme but still distinct
        self.placePawn(p1_r, p1_c, "#5D4037")  # Dark Brown Pawn
        self.placePawn(p2_r, p2_c, "#8D6E63")  # Light Brown Pawn

        # ▣ Side panel
        side_panel = QVBoxLayout()
        side_panel.setAlignment(Qt.AlignTop)

        self.label_turn = QLabel(f"Current Turn: {self.board_created.current_player}")
        self.label_turn.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #4E2A1E;
            padding: 10px;
            background-color: rgba(255, 248, 230, 0.85);
            border-radius: 12px;
        """)
        side_panel.addWidget(self.label_turn)

        # ▣ Buttons - wooden theme
        button_style = """
            QPushButton {
                background-color: #A97458;
                color: white;
                padding: 14px;
                border-radius: 16px;
                font-size: 19px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8B5A2B;
            }
        """

        reset_btn = QPushButton("Restart Game")
        reset_btn.setStyleSheet(button_style)
        reset_btn.clicked.connect(self.resetGame)

        back_btn = QPushButton("Back to Menu")
        back_btn.setStyleSheet(button_style)

        side_panel.addSpacing(40)
        side_panel.addWidget(reset_btn)
        side_panel.addWidget(back_btn)

        main_layout.addLayout(board_container, stretch=5)
        main_layout.addLayout(side_panel, stretch=2)

        self.setLayout(main_layout)

    def handleCellClick(self):
        btn = self.sender()
        r = btn.property("row")
        c = btn.property("col")

        current_player = self.board_created.current_player
        old_r, old_c = self.board_created.pawns[current_player]

        # Pawn colors remain consistent:
        color = "#5D4037" if current_player == "P1" else "#8D6E63"

        moved = self.board_created.move_pawn(current_player, (r, c))

        if moved:
            self.clearCell(old_r, old_c)
            self.placePawn(r, c, color)
            self.label_turn.setText(f"Current Turn: {self.board_created.current_player}")
        else:
            print("Invalid move!")

    def clearCell(self, row, col):
        btn = self.cells[(row, col)]
        btn.setStyleSheet("""
            QPushButton {
                background-color: #F2DFC2;
                border: 2px solid #B79267;
                border-radius: 12px;
                min-width: 65px;
                min-height: 65px;
            }
        """)

    def placePawn(self, row, col, color):
        btn = self.cells[(row, col)]
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 32px;
                border: 3px solid #FFFFFF;
                min-width: 65px;
                min-height: 65px;
                box-shadow: 0px 0px 12px rgba(0,0,0,0.35);
            }}
        """)

    def resetGame(self):
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                self.clearCell(r, c)

        self.board_created = Board(self.mode == 'AI')

        p1_r, p1_c = self.board_created.pawns["P1"]
        p2_r, p2_c = self.board_created.pawns["P2"]

        self.placePawn(p1_r, p1_c, "#5D4037")
        self.placePawn(p2_r, p2_c, "#8D6E63")

        self.label_turn.setText(f"Current Turn: {self.board_created.current_player}")
