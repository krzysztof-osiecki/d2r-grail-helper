from PySide6.QtWidgets import QWidget, QGridLayout, QMainWindow, QLabel, QTabWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt, QTimer, QPoint
import logging
import time
from state.app import State
from state.session import CURRENT_SESSION
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    label: QLabel

    def __init__(self):
        super().__init__()
        State().subscribe(self.on_update_app_state)
        CURRENT_SESSION.subscribe_item_change(self.update_items_table)
        # Set window properties
        self.setWindowTitle("D2R Assistant")
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Window)
        # self.setAttribute(Qt.WA_TranslucentBackground) doesnt work for now
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget) 

        # Enable dragging
        self._drag_active = False
        self._drag_start_position = QPoint()

        self.init_timer()
        
        main_layout = self.main_tab_layout()
        main_tab = QWidget()
        main_tab.setLayout(main_layout)

        game_layout = self.game_tab_layout()
        game_tab = QWidget()
        game_tab.setLayout(game_layout)

        items_layout = self.items_tab_layout()
        items_tab = QWidget()
        items_tab.setLayout(items_layout)

        tab_widget = QTabWidget(self)
        tab_widget.addTab(main_tab, "Main")
        tab_widget.addTab(game_tab, "Game")
        tab_widget.addTab(items_tab, "Items")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        self.central_widget.setLayout(main_layout)
        self.resize(300, 300)

    def items_tab_layout(self):
        grid_layout = QGridLayout(self)
        # Create the table widget
        self.items_table = QTableWidget()
        self.update_items_table(CURRENT_SESSION.items_saved)
        grid_layout.addWidget(self.items_table)
        return grid_layout

    def update_items_table(self, items_saved):
        if len(items_saved) > 0:
            self.items_table.setRowCount(len(items_saved))  # Set number of rows
            self.items_table.setColumnCount(len(items_saved[0].index))  # Set number of columns
            self.items_table.setHorizontalHeaderLabels(items_saved[0].index.tolist())  # Set column headers

        # Populate the table with data
        for row_index, series in enumerate(items_saved):
            for col_index, (key, value) in enumerate(series.items()):
                self.items_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))

    def game_tab_layout(self):
        grid_layout = QGridLayout(self)
        self.game_time = QLabel("Not in game...", self)
        grid_layout.addWidget(self.game_time)
        return grid_layout

    def main_tab_layout(self):
        grid_layout = QGridLayout(self)

        self.session_time = QLabel("Timer is starting...", self)
        grid_layout.addWidget(self.session_time)

        self.location_state = QLabel(f"{State()}", self)
        self.location_state.setAlignment(Qt.AlignCenter) 
        grid_layout.addWidget(self.location_state)

        self.session_state = QLabel(f"{CURRENT_SESSION}", self)
        self.session_state.setAlignment(Qt.AlignCenter)  
        grid_layout.addWidget(self.session_state)

        return grid_layout

    def init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_update_timer)
        self.timer.start(1000)


    def on_update_timer(self): 
        if State().in_game:
            CURRENT_SESSION.seconds_in_game += 1
        else:
            CURRENT_SESSION.seconds_out_of_game += 1

        # Get the current time and calculate the elapsed time
        current_time = time.time()
        
        # Calculate session time
        session_time = current_time - CURRENT_SESSION.session_start
        sessionString = self.format_time(session_time)
        self.session_time.setText(f"Session time: {sessionString}")

        # Calculate game time
        if CURRENT_SESSION.game_start != None:
            game_time = current_time - CURRENT_SESSION.game_start
            gameString = self.format_time(game_time)
            self.game_time.setText(f"Game time: {gameString}")
        else:
            self.game_time.setText(f"Not in game")

    def format_time(self, elapsed_time):
        # Convert the float time into minutes and seconds format
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        return f"{minutes:02}:{seconds:02}"
    
    def on_update_app_state(self, state : State, changed_property):
        self.location_state.setText(f"{State()}")
        self.session_state.setText(f"{CURRENT_SESSION}")

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
