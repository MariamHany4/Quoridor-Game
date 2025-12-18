from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Core.board import Board

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Ai.ai_player import AIPlayer

class BoardView(QWidget):
    # Signal to go back to main menu
    backToMenu = pyqtSignal()

    GRID_SIZE = 9

    def __init__(self, mode, difficulty="easy"):
        """
         Constructor - executes when creating an object from the class
        """

        super().__init__()
        self.mode = mode
        self.difficulty = difficulty
        self.undo_stack = []
        self.redo_stack = []

        self.setWindowTitle("Quoridor - Game Board")
        self.setGeometry(600, 200, 980, 900)

        self.cells = {}
        self.wall_labels = []
        self.board_created = Board(self.mode == 'AI')

        # Make window frameless
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Wall placement variables
        self.action_mode = "move"
        self.wall_orientation = "H"


        self.initUI()
        if self.mode == "AI":
            self.ai_player_obj = AIPlayer(player="P2", difficulty=self.difficulty)

    def initUI(self):
        """
        Build the user interface (UI)
        """
        # ===== Create Title Bar =====
        self.createTitleBar()

        # ===== Main Layout =====
        main_layout_wrapper = QVBoxLayout()
        main_layout_wrapper.setContentsMargins(0, 0, 0, 0)
        main_layout_wrapper.setSpacing(0)

        main_layout_wrapper.addWidget(self.title_bar)

        main_layout = QHBoxLayout()
        board_container = QVBoxLayout()

        # Global Style
        self.setStyleSheet("""
        QWidget {
            background: qradialgradient(
                cx:0.5, cy:0.3, radius:1.2,
                stop:0 #FFE4F5,
                stop:0.5 #FFB3D9,
                stop:1 #E91E63
            );
        }
        QLabel {
            font-family: 'Segoe UI';
        }
        """)

        # Title
        title = QLabel(f"Quoridor - {self.mode} Mode")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
        font-size: 36px;
        font-weight: 900;
        letter-spacing: 1px;
        color: #880E4F;
        padding: 18px;
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 #FFF0F7,
            stop:1 #FFD6E8
        );
        border-radius: 18px;
        border: 3px solid #C2185B;
        """)
        board_container.addWidget(title)

        # Board Grid
        grid_widget = QWidget()
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        tile_style = """
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #FFE4F5,
                stop:1 #FFC1E3
            );
            border: 2px solid #F06292;
            border-radius: 16px;
            min-width: 68px;
            min-height: 68px;
        }
        QPushButton:hover {
            background: #FFD6E8;
            border: 2px solid #EC407A;
        }
        """

        # Create cells (9x9)
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                btn = QPushButton()
                btn.setStyleSheet(tile_style)
                btn.setProperty("row", r)
                btn.setProperty("col", c)
                btn.clicked.connect(self.handleCellClick)

                self.addShadow(btn, blur=10, x=3, y=3)

                self.cells[(r, c)] = btn
                grid_layout.addWidget(btn, r, c)

        grid_widget.setLayout(grid_layout)
        board_container.addWidget(grid_widget)

        # Place Initial Pawns
        p1_r, p1_c = self.board_created.pawns["P1"]
        p2_r, p2_c = self.board_created.pawns["P2"]

        self.placePawn(p1_r, p1_c, "#AD1457")
        self.placePawn(p2_r, p2_c, "#F48FB1")

        # Side Panel
        side_panel = QVBoxLayout()
        side_panel.setAlignment(Qt.AlignTop)

        # Current turn label
        self.label_turn = QLabel(f"Current Turn: {self.board_created.current_player}")
        self.label_turn.setStyleSheet("""
        font-size: 24px;
        font-weight: bold;
        color: #880E4F;
        padding: 14px;
        background-color: rgba(255,240,247,0.95);
        border-radius: 16px;
        border: 2px solid #C2185B;
        """)
        side_panel.addWidget(self.label_turn)

        # Walls remaining label
        self.label_walls = QLabel(
            f"P1 Walls: {self.board_created.walls_left['P1']} | "
            f"P2 Walls: {self.board_created.walls_left['P2']}"
        )
        self.label_walls.setStyleSheet("""
        font-size: 18px;
        font-weight: bold;
        color: #880E4F;
        padding: 10px;
        background-color: rgba(255,240,247,0.95);
        border-radius: 12px;
        border: 2px solid #C2185B;
        """)
        side_panel.addWidget(self.label_walls)

        side_panel.addSpacing(20)

        # Mode Selection Label
        mode_label = QLabel("Action Mode:")
        mode_label.setStyleSheet("""
        font-size: 20px;
        font-weight: bold;
        color: #880E4F;
        padding: 10px;
        """)
        side_panel.addWidget(mode_label)

        # Move Mode Button
        self.btn_move_mode = QPushButton("Move Pawn")
        self.btn_move_mode.setStyleSheet("""
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #4CAF50,
                stop:1 #2E7D32
            );
            color: white;
            padding: 12px;
            border-radius: 16px;
            font-size: 18px;
            font-weight: bold;
            border: 3px solid #1B5E20;
        }
        QPushButton:hover {
            background: #66BB6A;
        }
        """)
        self.btn_move_mode.clicked.connect(self.setMoveMode)
        side_panel.addWidget(self.btn_move_mode)

        # Wall Mode Button
        self.btn_wall_mode = QPushButton("Place Wall")
        self.btn_wall_mode.setStyleSheet("""
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #F48FB1,
                stop:1 #E91E63
            );
            color: white;
            padding: 12px;
            border-radius: 16px;
            font-size: 18px;
            font-weight: bold;
            border: 2px solid #880E4F;
        }
        QPushButton:hover {
            background: #EC407A;
        }
        """)
        self.btn_wall_mode.clicked.connect(self.setWallMode)
        side_panel.addWidget(self.btn_wall_mode)

        side_panel.addSpacing(15)

        # Wall orientation label
        orientation_label = QLabel("Wall Direction:")
        orientation_label.setStyleSheet("""
        font-size: 18px;
        font-weight: bold;
        color: #880E4F;
        padding: 8px;
        """)
        side_panel.addWidget(orientation_label)

        # Toggle Orientation Button
        self.btn_orientation = QPushButton("Horizontal")
        self.btn_orientation.setStyleSheet("""
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #FFB3D9,
                stop:1 #F48FB1
            );
            color: #880E4F;
            padding: 10px;
            border-radius: 14px;
            font-size: 16px;
            font-weight: bold;
            border: 2px solid #C2185B;
        }
        QPushButton:hover {
            background: #F8BBD0;
        }
        """)
        self.btn_orientation.clicked.connect(self.toggleOrientation)
        side_panel.addWidget(self.btn_orientation)

        side_panel.addSpacing(30)

        # Game Control Buttons
        button_style = """
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #EC407A,
                stop:1 #AD1457
            );
            color: #FFF0F7;
            padding: 16px;
            border-radius: 20px;
            font-size: 20px;
            font-weight: bold;
            border: 2px solid #880E4F;
        }
        QPushButton:hover {
            background: #C2185B;
        }
        """

        reset_btn = QPushButton("Restart Game")
        reset_btn.setStyleSheet(button_style)
        reset_btn.clicked.connect(self.resetGame)

        back_btn = QPushButton("Back to Menu")
        back_btn.setStyleSheet(button_style)

        back_btn.clicked.connect(self.goBackToMenu)

        side_panel.addWidget(reset_btn)
        side_panel.addWidget(back_btn)

        # Assemble Main Layout
        main_layout.addLayout(board_container, stretch=5)
        main_layout.addLayout(side_panel, stretch=2)

        # Assemble everything
        content_widget = QWidget()
        content_widget.setLayout(main_layout)

        main_layout_wrapper.addWidget(content_widget)
        self.setLayout(main_layout_wrapper)

        # Game Control Buttons Style (same as Restart / Back)
        control_button_style = """
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #EC407A,
                stop:1 #AD1457
            );
            color: #FFF0F7;
            padding: 16px;
            border-radius: 20px;
            font-size: 20px;
            font-weight: bold;
            border: 2px solid #880E4F;
        }
        QPushButton:hover {
            background: #C2185B;
        }
        """

        # Undo button
        undo_btn = QPushButton("Undo")
        undo_btn.setStyleSheet(control_button_style)
        undo_btn.clicked.connect(self.undo)

        # Redo button
        redo_btn = QPushButton("Redo")
        redo_btn.setStyleSheet(control_button_style)
        redo_btn.clicked.connect(self.redo)

        # Add to side panel
        side_panel.addWidget(undo_btn)
        side_panel.addWidget(redo_btn)

    def createTitleBar(self):
        """
                    Create custom title bar like start screen
                    """
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("""
                             background: qlineargradient(
                                 x1:0, y1:0, x2:0, y2:1,
                                 stop:0 #E91E63,
                                 stop:1 #C2185B
                             );
                         """)

        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.setSpacing(5)

        # Icon
        icon_label = QLabel()
        icon_label.setFixedSize(24, 24)
        icon_label.setStyleSheet("""
                             QLabel {
                                 background: qradialgradient(
                                     cx:0.5, cy:0.5, radius:0.5,
                                     stop:0 white,
                                     stop:1 #FF4081
                                 );
                                 border-radius: 12px;
                                 border: 2px solid #880E4F;
                             }
                         """)

        # Title
        title_label = QLabel("Quoridor Game")
        title_label.setStyleSheet("""
                             QLabel {
                                 color: white;
                                 font-size: 14px;
                                 font-weight: bold;
                                 padding-left: 10px;
                             }
                         """)

        # Buttons
        minimize_btn = self.createControlButton("🗕", "#F48FB1", "#EC407A")
        minimize_btn.setFixedSize(28, 28)
        minimize_btn.clicked.connect(self.showMinimized)

        maximize_btn = self.createControlButton("🗖", "#F48FB1", "#EC407A")
        maximize_btn.setFixedSize(28, 28)
        maximize_btn.clicked.connect(self.toggleMaximize)
        self.is_maximized = False
        self.maximize_btn = maximize_btn

        close_btn = self.createControlButton("✕", "#FF5252", "#D32F2F")
        close_btn.setFixedSize(28, 28)
        close_btn.clicked.connect(self.close)

        # Add to layout
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        title_layout.addWidget(minimize_btn)
        title_layout.addWidget(maximize_btn)
        title_layout.addWidget(close_btn)

        self.title_bar.setLayout(title_layout)

    def createControlButton(self, text, color1, color2):
            """
            Create title bar button
            """
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(
                        x1:0, y1:0, x2:0, y2:1,
                        stop:0 {color1},
                        stop:1 {color2}
                    );
                    color: white;
                    border-radius: 14px;
                    font-size: 16px;
                    font-weight: bold;
                    border: none;
                }}
                QPushButton:hover {{
                    background: #EC407A;
                }}
                QPushButton:pressed {{
                    background: #C2185B;
                }}
            """)
            return btn

    def toggleMaximize(self):
            """
            Toggle maximize/normal
            """
            if self.is_maximized:
                self.showNormal()
                self.maximize_btn.setText("🗖")
            else:
                self.showMaximized()
                self.maximize_btn.setText("🗗")
            self.is_maximized = not self.is_maximized

    def mousePressEvent(self, event):
            """
            Enable dragging window
            """
            if event.button() == Qt.LeftButton:
                self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()

    def mouseMoveEvent(self, event):
            """
            Move window when dragging
            """
            if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_position'):
                self.move(event.globalPos() - self.drag_position)
                event.accept()

    def handleCellClick(self):
        """
        Executes when a player clicks on a cell.
        Handles both human and AI turns automatically in AI mode.
        """
        btn = self.sender()
        r = btn.property("row")
        c = btn.property("col")

        current_player = self.board_created.current_player

        # ===== Block human clicks during AI turn =====
        if self.mode == "AI" and current_player == "P2":
            return

        # ===== MOVE MODE =====
        if self.action_mode == "move":

            old_r, old_c = self.board_created.pawns[current_player]
            color = "#AD1457" if current_player == "P1" else "#F48FB1"

            moved = self.board_created.move_pawn(current_player, (r, c))
            if moved:
                if moved:
                    # Save action for undo
                    self.undo_stack.append({
                        "type": "move",
                        "player": current_player,
                        "from": (old_r, old_c),
                        "to": (r, c)
                    })
                    self.redo_stack.clear()  # Clear redo after new action

                # Update board UI
                self.clearCell(old_r, old_c)
                self.placePawn(r, c, color)

                # Update turn label
                self.label_turn.setText(f"Current Turn: {self.board_created.current_player}")

                # Check winner
                winner = self.checkWinner(current_player, r)
                if winner:
                    self.showSimpleWinner(winner)
                    return  # Stop further actions if game ended

                print(f"{current_player} moved to ({r}, {c})")

                # ===== Trigger AI if next turn =====
                if self.mode == "AI" and self.board_created.current_player == "P2":
                    QTimer.singleShot(300, self.ai_move)
            else:
                print(f"Invalid move!")

        # ===== WALL MODE =====
        elif self.action_mode == "wall":
            placing_player = current_player

            placed = self.board_created.place_wall(
                current_player,
                r,
                c,
                self.wall_orientation
            )

            if placed:
                if placed:
                    self.undo_stack.append({
                        "type": "wall",
                        "player": current_player,
                        "pos": (r, c),
                        "orientation": self.wall_orientation
                    })
                    self.redo_stack.clear()  # Clear redo after new action

                print(f"{placing_player} placed wall at ({r}, {c}) - {self.wall_orientation}")
                self.drawWall(r, c, self.wall_orientation, placing_player)
                self.label_turn.setText(f"Current Turn: {self.board_created.current_player}")
                self.updateWallsLabel()

                # ===== Trigger AI if next turn =====
                if self.mode == "AI" and self.board_created.current_player == "P2":
                    QTimer.singleShot(300, self.ai_move)
            else:
                print(f"Cannot place wall at ({r}, {c})")
        # After human move in "move" mode


    def drawWall(self, x, y, orientation, player):
        """
        Draw beautiful wall with player colors - CORRECT PLAYER
        """
        # Use the player parameter directly (no need to reverse)
        wall_player = player

        # Colors for each player
        if wall_player == "P1":
            # Player 1 - BRIGHTER Dark Pink
            wall_color = "#D81B60"
            gradient_start = "#EC407A"
            gradient_end = "#AD1457"
            border_color = "#880E4F"
            shadow_color = QColor(216, 27, 96, 220)
        else:
            # Player 2 - BRIGHTER Light Pink
            wall_color = "#FF80AB"
            gradient_start = "#FFB3D9"
            gradient_end = "#F48FB1"
            border_color = "#F06292"
            shadow_color = QColor(255, 128, 171, 220)

        # Create wall with gradient
        wall = QLabel(self)

        if orientation == "H":
            wall.setStyleSheet(f"""
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 {gradient_start},
                stop:0.5 {wall_color},
                stop:1 {gradient_end}
            );
            border-radius: 3px;
            border: 2px solid {border_color};
            """)
        else:
            wall.setStyleSheet(f"""
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 {gradient_start},
                stop:0.5 {wall_color},
                stop:1 {gradient_end}
            );
            border-radius: 3px;
            border: 2px solid {border_color};
            """)

        # Get the cell
        cell1 = self.cells[(x, y)]

        # Get positions
        global_pos1 = cell1.mapToGlobal(QPoint(0, 0))
        local_pos1 = self.mapFromGlobal(global_pos1)

        # Cell dimensions
        cell_width = cell1.width()
        cell_height = cell1.height()

        # Grid spacing - FULL SIZE
        spacing = 10

        if orientation == "H":
            # Horizontal wall - FILLS THE GAP
            wall_x = local_pos1.x()
            wall_y = local_pos1.y() + cell_height
            wall_width = cell_width * 2 + spacing
            wall_height = spacing

            wall.setGeometry(wall_x, wall_y, wall_width, wall_height)

        else:  # Vertical
            # Vertical wall - FILLS THE GAP
            wall_x = local_pos1.x() + cell_width
            wall_y = local_pos1.y()
            wall_width = spacing
            wall_height = cell_height * 2 + spacing

            wall.setGeometry(wall_x, wall_y, wall_width, wall_height)

        # Add glow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(12)
        shadow.setOffset(0, 0)
        shadow.setColor(shadow_color)
        wall.setGraphicsEffect(shadow)

        wall.show()
        wall.raise_()

        self.wall_labels.append(wall)

        print(f"{wall_player} placed {orientation} wall at ({x},{y})")

    def updateWallsLabel(self):
        """
        Update walls counter
        """
        self.label_walls.setText(
            f"P1 Walls: {self.board_created.walls_left['P1']} | "
            f"P2 Walls: {self.board_created.walls_left['P2']}"
        )


    def clearCell(self, row, col):
        """
        Clear cell content
        """
        btn = self.cells[(row, col)]
        btn.setGraphicsEffect(None)
        btn.setStyleSheet("""
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #FFE4F5,
                stop:1 #FFC1E3
            );
            border: 2px solid #F06292;
            border-radius: 16px;
            min-width: 68px;
            min-height: 68px;
        }
        """)
        self.addShadow(btn, blur=10, x=3, y=3)

    def placePawn(self, row, col, base_color):
        """
        Place a pawn in a cell
        """
        btn = self.cells[(row, col)]
        btn.setGraphicsEffect(None)

        btn.setStyleSheet(f"""
        QPushButton {{
            background: qradialgradient(
                cx:0.3, cy:0.3, radius:0.8,
                stop:0 #FFFFFF,
                stop:0.35 {base_color},
                stop:1 #880E4F
            );
            border-radius: 34px;
            border: 4px solid #FFF0F7;
            min-width: 68px;
            min-height: 68px;
        }}
        """)

        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(25)
        glow.setOffset(0, 0)
        glow.setColor(QColor(255, 192, 227, 180))
        btn.setGraphicsEffect(glow)

    def addShadow(self, widget, blur=12, x=2, y=2):
        """
        Add shadow to widget
        """
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur)
        shadow.setOffset(x, y)
        shadow.setColor(QColor(233, 30, 99, 120))
        widget.setGraphicsEffect(shadow)

    def resetGame(self):
        """
        Restart game
        """
        # Clear all cells
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                self.clearCell(r, c)

        # Clear walls
        for wall in self.wall_labels:
            wall.deleteLater()
        self.wall_labels.clear()

        # Create new board
        self.board_created = Board(self.mode == 'AI')
        if self.mode == "AI":
            self.ai_player_obj = AIPlayer(
                player="P2",
                difficulty=self.difficulty
            )

        # Place pawns
        p1_r, p1_c = self.board_created.pawns["P1"]
        p2_r, p2_c = self.board_created.pawns["P2"]

        self.placePawn(p1_r, p1_c, "#AD1457")
        self.placePawn(p2_r, p2_c, "#F48FB1")

        # Update labels
        self.label_turn.setText(f"Current Turn: {self.board_created.current_player}")
        self.updateWallsLabel()

   

    def setMoveMode(self):
        """
        Switch to Move mode
        """
        self.action_mode = "move"
        print("Mode: Move Pawn")

        # Highlight move button
        self.btn_move_mode.setStyleSheet("""
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #4CAF50,
                stop:1 #2E7D32
            );
            color: white;
            padding: 12px;
            border-radius: 16px;
            font-size: 18px;
            font-weight: bold;
            border: 3px solid #1B5E20;
        }
        """)

        # Reset wall button
        self.btn_wall_mode.setStyleSheet("""
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #F48FB1,
                stop:1 #E91E63
            );
            color: white;
            padding: 12px;
            border-radius: 16px;
            font-size: 18px;
            font-weight: bold;
            border: 2px solid #880E4F;
        }
        """)

    def setWallMode(self):
        """
        Switch to Wall mode
        """
        self.action_mode = "wall"
        print("Mode: Place Wall")

        # Highlight wall button
        self.btn_wall_mode.setStyleSheet("""
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #4CAF50,
                stop:1 #2E7D32
            );
            color: white;
            padding: 12px;
            border-radius: 16px;
            font-size: 18px;
            font-weight: bold;
            border: 3px solid #1B5E20;
        }
        """)

        # Reset move button
        self.btn_move_mode.setStyleSheet("""
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #F8BBD0,
                stop:1 #EC407A
            );
            color: white;
            padding: 12px;
            border-radius: 16px;
            font-size: 18px;
            font-weight: bold;
            border: 2px solid #C2185B;
        }
        """)

    def toggleOrientation(self):
        """
        Toggle wall orientation
        """
        if self.wall_orientation == "H":
            self.wall_orientation = "V"
            self.btn_orientation.setText("Vertical")
            print("Orientation: Vertical")
        else:
            self.wall_orientation = "H"
            self.btn_orientation.setText("Horizontal")
            print("Orientation: Horizontal")

    def checkWinner(self, player, row):
        """
        Check if player reached their goal
        """
        # P1 needs to reach row 8 (bottom)
        if player == "P1" and row == 8:
            return "P1"
        # P2 needs to reach row 0 (top)
        elif player == "P2" and row == 0:
            return "P2"
        return None

    def showSimpleWinner(self, winner):
        """
        Show simple winner message
        """
        if winner == "P1":
            player_name = "Player 1"
        else:
            player_name = "Player 2"

        # Simple message box
        msg = QMessageBox(self)
        msg.setWindowTitle("Game Over!")
        msg.setText(f" {player_name} WINS! ")
        msg.setInformativeText("Congratulations!")
        msg.setIcon(QMessageBox.Information)

        # Buttons
        play_again = msg.addButton("Play Again", QMessageBox.AcceptRole)
        main_menu = msg.addButton("Main Menu", QMessageBox.RejectRole)

        msg.setStyleSheet("""
        QMessageBox {
            background: #FFE4F5;
        }
        QLabel {
            color: #880E4F;
            font-size: 18px;
            font-weight: bold;
        }
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #F48FB1,
                stop:1 #E91E63
            );
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: bold;
            min-width: 100px;
        }
        QPushButton:hover {
            background: #EC407A;
        }
        """)

        msg.exec_()

        # Handle button click
        if msg.clickedButton() == play_again:
            self.resetGame()
        elif msg.clickedButton() == main_menu:
            self.goBackToMenu()

    def goBackToMenu(self):
        """
        Go back to main menu
        """
        self.backToMenu.emit() 
        self.close()  # Close board window

    def ai_move(self):
        if self.mode != "AI" or self.board_created.current_player != "P2":
            return

        action = self.ai_player_obj.choose_action(self.board_created)
        if action is None:
            return

        self.executeAction(action)

    def executeAction(self, action):
        """
        Execute an AI action (move or wall) safely.
        """

        current_player = self.board_created.current_player
        ai_color = "#F48FB1"  # AI pawn color (P2)

        if action["type"] == "move":
            old_r, old_c = self.board_created.pawns[current_player]
            new_pos = action.get("to")

            if new_pos and self.board_created.move_pawn(current_player, new_pos):
                # Save for undo
                self.undo_stack.append({
                    "type": "move",
                    "player": current_player,
                    "from": (old_r, old_c),
                    "to": new_pos
                })
                self.redo_stack.clear()

                # Update UI
                self.clearCell(old_r, old_c)
                r, c = new_pos
                self.placePawn(r, c, ai_color)
                self.label_turn.setText(f"Current Turn: {self.board_created.current_player}")

                # Check winner
                winner = self.checkWinner(current_player, r)
                if winner:
                    self.showSimpleWinner(winner)
            else:
                print("AI tried invalid move!")


        elif action["type"] == "wall":

            x, y = action.get("x"), action.get("y")

            orientation = action.get("orientation")

            if None not in (x, y, orientation) and self.board_created.place_wall(current_player, x, y, orientation):

                # Save for undo

                self.undo_stack.append({

                    "type": "wall",

                    "player": current_player,

                    "pos": (x, y),

                    "orientation": orientation

                })

                self.redo_stack.clear()

                self.drawWall(x, y, orientation, current_player)

                self.label_turn.setText(f"Current Turn: {self.board_created.current_player}")

                self.updateWallsLabel()

            else:
                print("AI tried invalid wall placement!")

    def undo(self):
        if not self.undo_stack:
            return

        action = self.undo_stack.pop()
        self.redo_stack.append(action)

        player = action["player"]

        if action["type"] == "move":
            # Move back
            self.clearCell(*action["to"])
            self.placePawn(*action["from"], "#AD1457" if player == "P1" else "#F48FB1")
            self.board_created.pawns[player] = action["from"]
            self.board_created.current_player = player

        elif action["type"] == "wall":
            # Remove wall visually and from board
            self.removeWall(action["pos"], action["orientation"], player)
            self.board_created.remove_wall(player, action["pos"], action["orientation"])

        self.label_turn.setText(f"Current Turn: {self.board_created.current_player}")
        self.updateWallsLabel()

    def redo(self):
        if not self.redo_stack:
            return

        action = self.redo_stack.pop()
        self.undo_stack.append(action)

        player = action["player"]

        if action["type"] == "move":
            self.clearCell(*action["from"])
            self.placePawn(*action["to"], "#AD1457" if player == "P1" else "#F48FB1")
            self.board_created.pawns[player] = action["to"]
            self.board_created.current_player = player



        elif action["type"] == "wall":

            self.drawWall(*action["pos"], action["orientation"], player)

            self.board_created.place_wall(player, *action["pos"], action["orientation"])

            self.board_created.current_player = player

        self.label_turn.setText(f"Current Turn: {self.board_created.current_player}")
        self.updateWallsLabel()

    def removeWall(self, pos, orientation, player):
        x, y = pos
        for wall in self.wall_labels:
            if wall.property("x") == x and wall.property("y") == y and wall.property("orientation") == orientation:
                wall.deleteLater()
                self.wall_labels.remove(wall)
                break

        # Remove from board data
        try:
            self.board_created.remove_wall(player, pos, orientation)
        except Exception as e:
            print(f"Error removing wall from board: {e}")

        self.updateWallsLabel()
