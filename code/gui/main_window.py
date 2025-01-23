from PySide6.QtWidgets import QWidget, QMainWindow, QLabel, QTabWidget, QVBoxLayout, QApplication, QPushButton
from PySide6.QtCore import Qt, QTimer, QPoint, QThread, QTimer, QObject, Signal
from gui.profile_session_tab import ProfileSessionTab
from gui.main_tab import MainTab
from gui.stats_tab import StatsTab
from gui.added_item import AddedItemNotification
from gui.select_item import SelectItemNotification
from gui.css import get_application_stylesheet
from event.event_manager import EventManager, EventType
import logging

logger = logging.getLogger(__name__)

class ItemAddWorker(QObject):
    notify = Signal(dict)

    def notify_with_last_added_item(self, item):
        self.notify.emit(item)

class ManualAddItemWorker(QObject):
    notify = Signal()

    def notify_show_add_item_window_from_event(self, _):
        self.notify.emit()

    def notify_show_add_item_window(self):
        self.notify.emit()

class MainWindow(QMainWindow):
    label: QLabel

    def __init__(self):
        super().__init__()
        self.worker_thread = QThread()
        self.item_add_worker = ItemAddWorker()
        self.item_add_worker.moveToThread(self.worker_thread)
        self.item_add_worker.notify.connect(self.show_item_added_toast)
        self.manual_add_item_worker = ManualAddItemWorker()
        self.manual_add_item_worker.moveToThread(self.worker_thread)
        self.manual_add_item_worker.notify.connect(self.show_add_item_window)
        self.worker_thread.start()

        EventManager().subscribe(EventType.REQUEST_ADD_ITEM, self.manual_add_item_worker.notify_show_add_item_window_from_event)

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

        # Close button
        self.close_button = QPushButton("✖", self)
        self.close_button.setStyleSheet("""
            QPushButton {
                color: red;
                background-color: transparent;                                      
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                color: darkred;
            }
        """)
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.setFixedSize(50, 50)  # Set a fixed size for the button
        self.close_button.move(self.width() - self.close_button.width() + 10, 0)
        # Connect the button to the close function
        self.close_button.clicked.connect(self.close)

        # tabs
        self.main_tab = MainTab()
        self.items_tab = ProfileSessionTab(self)
        self.stats_tab = StatsTab()

        tab_widget = QTabWidget(self)
        tab_widget.addTab(self.main_tab, "Main")
        tab_widget.addTab(self.items_tab, "Profile/Session")
        tab_widget.addTab(self.stats_tab, "Stats")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        self.central_widget.setLayout(main_layout)
        self.resize(300, 300)

        # Get the screen geometry
        screen_geometry = QApplication.primaryScreen().availableGeometry()

        # Calculate the bottom-left corner position
        x_position = screen_geometry.left() + 2  # Left edge of the screen
        y_position = screen_geometry.bottom() - self.height()  # Bottom edge minus window height

        # Move the window to the bottom-left corner
        self.move(x_position, y_position)

    def init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_update_timer)
        self.timer.start(1000)

    def on_update_timer(self): 
        self.main_tab.update()

    def resizeEvent(self, event):
        """Reposition the close button on window resize."""
        super().resizeEvent(event)
        # Position the button at the top-right corner, with 10px padding from the edge
        self.close_button.move(self.width() - self.close_button.width() + 10, 0)

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

    def show_item_added_toast(self, saved_item):
        toast = AddedItemNotification(self, saved_item)
        toast.show_notification()

    def show_add_item_window(self):
        toast = SelectItemNotification(self)
        toast.show_notification()
