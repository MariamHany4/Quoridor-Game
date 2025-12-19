from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from GUI.board_screen import BoardView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quoridor Game")
        # Set window size first
        self.resize(950, 820)

        # Get screen geometry
        screen = QGuiApplication.primaryScreen()
        screen_geometry = screen.geometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Calculate x, y to center the window
        x = (screen_width - self.width()) // 2
        y = (screen_height - self.height()) // 2

        # Move the window to the center
        self.move(x, y)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.createControlButtons()

        self.ai_player = QPushButton("Play vs AI")
        self.human_player = QPushButton("Play vs Human")
        self.easy_btn = QPushButton("EASY")
        self.medium_btn = QPushButton("MEDIUM")
        self.hard_btn = QPushButton("HARD")
        self.difficulty_group = QButtonGroup(self)
        self.difficulty_group.setExclusive(True)  # only one button can be selected at a time
        for btn in [self.easy_btn, self.medium_btn, self.hard_btn]:
            self.difficulty_group.addButton(btn)

        for btn in [self.easy_btn, self.medium_btn, self.hard_btn]:
            btn.setCheckable(True)
            for btn in [self.easy_btn, self.medium_btn, self.hard_btn]:
                btn.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(
                            x1:0, y1:0, x2:0, y2:1,
                            stop:0 #F48FB1,
                            stop:1 #E91E63
                        );
                        color: white;
                        padding: 14px 30px;
                        font-size: 20px;
                        font-weight: bold;
                        border-radius: 18px;
                        border: 3px solid #AD1457;
                    }
                    QPushButton:hover {
                        background: #EC407A;
                    }
                    QPushButton:pressed {
                        background: #C2185B;
                    }
                    QPushButton:checked {
                        background: #880E4F;    /* selected color */
                        border: 3px solid #FFC107;
                    }
                """)

            self.addShadow(btn, blur=20, x=0, y=6)
            btn.hide()  # hide initially

        # Connect buttons
        self.easy_btn.clicked.connect(lambda: self.start_ai("easy"))
        self.medium_btn.clicked.connect(lambda: self.start_ai("medium"))
        self.hard_btn.clicked.connect(lambda: self.start_ai("hard"))

        self.initUI()

        self.ai_player.clicked.connect(self.show_difficulty_options)
        self.human_player.clicked.connect(self.open_human_mode)

    def createControlButtons(self):

        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40)
        self.title_bar.setStyleSheet("""
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #E91E63,
                stop:1 #C2185B
            );
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """)

        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(10, 0, 10, 0)
        title_layout.setSpacing(5)

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

        self.title_label = QLabel("Quoridor Game")
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding-left: 10px;
            }
        """)

        self.minimize_btn = self.createControlButton("🗕", "#F48FB1", "#EC407A")
        self.minimize_btn.setFixedSize(28, 28)
        self.minimize_btn.clicked.connect(self.showMinimized)

        self.maximize_btn = self.createControlButton("🗖", "#F48FB1", "#EC407A")
        self.maximize_btn.setFixedSize(28, 28)
        self.maximize_btn.clicked.connect(self.toggleMaximize)
        self.is_maximized = False

        self.close_btn = self.createControlButton("✕", "#FF5252", "#D32F2F")
        self.close_btn.setFixedSize(28, 28)
        self.close_btn.clicked.connect(self.close)

        title_layout.addWidget(icon_label)
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()
        title_layout.addWidget(self.minimize_btn)
        title_layout.addWidget(self.maximize_btn)
        title_layout.addWidget(self.close_btn)

        self.title_bar.setLayout(title_layout)

    def createControlButton(self, text, color1, color2):

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

        if self.is_maximized:
            self.showNormal()
            self.maximize_btn.setText("🗖")
        else:
            self.showMaximized()
            self.maximize_btn.setText("🗗")
        self.is_maximized = not self.is_maximized

    def initUI(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_layout.addWidget(self.title_bar)

        content_widget = QWidget()
        content_widget.setStyleSheet("""
            QWidget {
                background: qradialgradient(
                    cx:0.5, cy:0.3, radius:1.4,
                    stop:0 #FFE4F5,
                    stop:0.5 #FFB3D9,
                    stop:1 #E91E63
                );
            }
        """)

        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)

        # ===== Main Card Frame =====
        frame = QFrame()
        frame.setStyleSheet("""
        QFrame {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 rgba(255, 255, 255, 0.95),
                stop:1 rgba(255, 240, 247, 0.95)
            );
            border-radius: 30px;
            padding: 45px;
            border: 4px solid #C2185B;
        }
        """)
        self.addShadow(frame, blur=35, x=0, y=12)

        # ===== Layout for frame =====
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # ===== Title & Subtitle =====
        title = QLabel("QUORIDOR")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 48px;
            font-weight: 900;
            letter-spacing: 4px;
            color: #880E4F;
        """)

        subtitle = QLabel("Choose Game Mode")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 38px;
            color: #C2185B;
            font-weight:bold;
            margin-bottom: 10px;
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(15)

        # ===== Main Buttons =====
        button_style = """
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:0, y2:1,
                stop:0 #F48FB1,
                stop:1 #E91E63
            );
            color: #FFFFFF;
            padding: 20px;
            font-size: 24px;
            font-weight: bold;
            border-radius: 22px;
            min-width: 280px;
            border: 3px solid #AD1457;
        }
        QPushButton:hover {
            background: #EC407A;
        }
        QPushButton:pressed {
            background: #C2185B;
        }
        """
        self.ai_player.setStyleSheet(button_style)
        self.human_player.setStyleSheet(button_style)
        self.addShadow(self.ai_player, blur=25, x=0, y=8)
        self.addShadow(self.human_player, blur=25, x=0, y=8)

        layout.addWidget(self.ai_player)
        layout.addWidget(self.human_player)

        # ===== Difficulty Buttons Layout =====
        self.difficulty_layout = QHBoxLayout()
        self.difficulty_layout.setAlignment(Qt.AlignCenter)

        for btn in [self.easy_btn, self.medium_btn, self.hard_btn]:
            btn.setCheckable(True)
            btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(
                        x1:0, y1:0, x2:0, y2:1,
                        stop:0 #F48FB1,
                        stop:1 #E91E63
                    );
                    color: white;
                    padding: 12px 24px;
                    font-size: 18px;
                    font-weight: bold;
                    border-radius: 18px;
                    border: 2px solid #AD1457;
                }
                QPushButton:hover {
                    background: #EC407A;
                }
                QPushButton:pressed {
                    background: #C2185B;
                }
                QPushButton:checked {
                    background: #880E4F;
                    border: 3px solid #FFC107;
                }
            """)
            self.addShadow(btn, blur=20, x=0, y=6)
            btn.hide()  # hide initially
            self.difficulty_layout.addWidget(btn)

        layout.addLayout(self.difficulty_layout)

        # ===== Set layout to frame and main content =====
        frame.setLayout(layout)
        content_layout.addWidget(frame)
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    # ===== Utilities =====
    def addShadow(self, widget, blur=20, x=0, y=6):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(blur)
        shadow.setOffset(x, y)
        shadow.setColor(QColor(136, 14, 79, 140))
        widget.setGraphicsEffect(shadow)

    # ===== دعم السحب للنافذة =====
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPos() - self.drag_position)
            event.accept()

    # ===== Navigation =====
    def open_ai_mode(self):
        # We no longer use combo_diff here
        self.show_difficulty_options()

    def open_human_mode(self):
        self.board = BoardView("HUMAN")
        self.board.backToMenu.connect(self.show)
        self.board.show()
        self.close()

    def show_difficulty_options(self):
        self.ai_player.hide()
        self.human_player.hide()
        for btn in [self.easy_btn, self.medium_btn, self.hard_btn]:
            btn.show()

    def start_ai(self, difficulty):
        from Ai.ai_player import AIPlayer
        self.ai_player_obj = AIPlayer("P2", difficulty)
        self.board = BoardView("AI", difficulty=difficulty)
        self.board.backToMenu.connect(self.show)
        self.board.show()
        self.close()


