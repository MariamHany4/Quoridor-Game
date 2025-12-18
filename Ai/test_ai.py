# test_ai_gui.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from Core.board import Board
from Ai.ai_player import AIPlayer

class QuoridorGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quoridor AI Test")
        self.board = Board(ai_opponent=True)
        self.ai_p1 = AIPlayer("P1", difficulty="medium")
        self.ai_p2 = AIPlayer("P2", difficulty="medium")
        self.grid_labels = [[QLabel() for _ in range(9)] for _ in range(9)]
        self.init_ui()
        self.update_board_ui()
        self.current_ai = self.ai_p1

        # Start AI moves automatically every 1 second
        self.timer = QTimer()
        self.timer.timeout.connect(self.ai_move)
        self.timer.start(1000)

    def init_ui(self):
        layout = QVBoxLayout()
        grid = QGridLayout()
        for r in range(9):
            for c in range(9):
                label = self.grid_labels[r][c]
                label.setFixedSize(50, 50)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("border: 1px solid black; font-size: 20px;")
                grid.addWidget(label, r, c)
        layout.addLayout(grid)
        self.setLayout(layout)

    def update_board_ui(self):
        for r in range(9):
            for c in range(9):
                self.grid_labels[r][c].setText(".")
        # Place pawns
        p1_r, p1_c = self.board.pawns["P1"]
        p2_r, p2_c = self.board.pawns["P2"]
        self.grid_labels[p1_r][p1_c].setText("1")
        self.grid_labels[p2_r][p2_c].setText("2")

        # Optionally, you can add wall visualization here

    def ai_move(self):
        if self.board.current_player == "P1":
            move = self.ai_p1.choose_action(self.board)
        else:
            move = self.ai_p2.choose_action(self.board)

        if move is None:
            QMessageBox.information(self, "Game Over", f"Player {self.board.current_player} has no moves!")
            self.timer.stop()
            return

        if move["type"] == "move":
            self.board.move_pawn(self.board.current_player, move["to"])
        else:
            self.board.place_wall(
                self.board.current_player,
                move["x"], move["y"], move["orientation"]
            )

        self.update_board_ui()

        # Check for win
        if self.board.pawns["P1"][0] == 8:
            QMessageBox.information(self, "Game Over", "P1 wins!")
            self.timer.stop()
        elif self.board.pawns["P2"][0] == 0:
            QMessageBox.information(self, "Game Over", "P2 wins!")
            self.timer.stop()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuoridorGUI()
    window.show()
    sys.exit(app.exec())
