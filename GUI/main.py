from PyQt5.QtWidgets import QApplication
import sys
from GUI.start_screen import MainWindow

def window():
    """
    Main function that initializes the application and starts the main window.
    """
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())




if __name__ =="__main__":
    window()
    