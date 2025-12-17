from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# ---------------- WINNER VIEW ----------------
class WinnerView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent

    def playAgain(self, dialog):
        """
        Reset game and close dialog
        """
        dialog.accept()  # Use accept instead of close
        if hasattr(self.parent_window, "resetGame"):
            self.parent_window.resetGame()

    def addShadow(self, widget, blur=25):
        """
        Add shadow effect to widget
        """
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(0, 0, 0, 180))
        widget.setGraphicsEffect(shadow)

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
        msg.setWindowTitle("🏆 Game Over!")
        msg.setText(f"🎉 {player_name} WINS! 🎉")
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


    def goToMainMenu(self, dialog):
        """
        Go back to main menu
        """
        dialog.accept()  # Use accept instead of close
        if self.parent_window:
            # Emit signal to show main menu
            if hasattr(self.parent_window, 'backToMenu'):
                self.parent_window.backToMenu.emit()
            self.parent_window.close()