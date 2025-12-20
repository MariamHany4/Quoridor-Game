# runner.py
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt  # <-- import Qt here
from GUI.start_screen import MainWindow  # Import main menu

def main():
    # Enable high-DPI scaling (optional, makes UI sharper on modern screens)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
