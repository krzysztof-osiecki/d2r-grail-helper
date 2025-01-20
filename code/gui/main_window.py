from PySide6.QtWidgets import QWidget, QMainWindow, QLabel, QTabWidget, QVBoxLayout, QApplication
from PySide6.QtCore import Qt, QTimer, QPoint
from gui.session_tab import SessionTab
from gui.items_tab import ItemsTab
from gui.game_tab import GameTab
from gui.main_tab import MainTab
from gui.css import get_application_stylesheet
import logging

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    label: QLabel

    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("D2R Assistant")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Window)
        self.setStyleSheet(get_application_stylesheet())
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget) 

        # Enable dragging
        self._drag_active = False
        self._drag_start_position = QPoint()

        self.init_timer()

        self.main_tab = MainTab()
        self.game_tab = GameTab()
        self.items_tab = ItemsTab()
        self.session_tab = SessionTab()

        tab_widget = QTabWidget(self)
        tab_widget.addTab(self.main_tab, "Main")
        tab_widget.addTab(self.game_tab, "Game")
        tab_widget.addTab(self.items_tab, "Items")
        tab_widget.addTab(self.session_tab, "Session")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        self.central_widget.setLayout(main_layout)
        self.resize(300, 300)

        # Get the screen geometry
        screen_geometry = QApplication.primaryScreen().availableGeometry()

        # Calculate the bottom-left corner position
        x_position = screen_geometry.left()  # Left edge of the screen
        y_position = screen_geometry.bottom() - self.height()  # Bottom edge minus window height

        # Move the window to the bottom-left corner
        self.move(x_position, y_position)

    def init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_update_timer)
        self.timer.start(1000)

    def on_update_timer(self): 
        self.main_tab.update()
        self.game_tab.update()

    def mousePressEvent(self, event):
        """Start dragging when the left mouse button is pressed"""
        if event.button() == Qt.LeftButton:
            self._drag_active = True
            self._drag_start_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        """Drag the window while the left mouse button is held"""
        if self._drag_active:
            new_position = self.pos() + (event.globalPosition().toPoint() - self._drag_start_position)
            self.move(new_position)
            self._drag_start_position = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        """Stop dragging when the left mouse button is released"""
        if event.button() == Qt.LeftButton:
            self._drag_active = False
