from PySide6.QtWidgets import QWidget, QGridLayout, QMainWindow, QLabel, QTabWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QApplication
from PySide6.QtCore import Qt, QTimer, QPoint
import logging
import time
from datetime import datetime, timedelta
from state.app import State
from state.session import CURRENT_SESSION
from gui.css import get_application_stylesheet
logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    label: QLabel

    def __init__(self):
        super().__init__()
        State().subscribe(self.on_update_app_state)
        CURRENT_SESSION.subscribe_item_change(self.update_items_table)
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

        # Get the screen geometry
        screen_geometry = QApplication.primaryScreen().availableGeometry()

        # Calculate the bottom-left corner position
        x_position = screen_geometry.left()  # Left edge of the screen
        y_position = screen_geometry.bottom() - self.height()  # Bottom edge minus window height

        # Move the window to the bottom-left corner
        self.move(x_position, y_position)

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

        self.session_start = QLabel(f"Session started {CURRENT_SESSION.session_start.strftime("%Y-%m-%d %H:%M:%S")}", self)
        self.session_start.setAlignment(Qt.AlignCenter)  

        self.session_time = QLabel("Timer is starting...", self)
        self.session_time.setAlignment(Qt.AlignCenter) 


        self.location_state = QLabel(f"{State()}", self)
        self.location_state.setAlignment(Qt.AlignCenter) 

        self.number_of_games = QLabel(f"Games joined: 0", self)
        self.number_of_games.setAlignment(Qt.AlignCenter)  
            
        self.percentage_of_time_in_game = QLabel(f"Time in-game: 0%", self)
        self.percentage_of_time_in_game.setAlignment(Qt.AlignCenter)  

        grid_layout.addWidget(self.session_start)
        grid_layout.addWidget(self.session_time)
        grid_layout.addWidget(self.location_state)
        grid_layout.addWidget(self.number_of_games)
        grid_layout.addWidget(self.percentage_of_time_in_game)

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
        current_time = datetime.now()
        
        # Calculate session time
        session_time = current_time - CURRENT_SESSION.session_start
        sessionString = self.format_time(session_time)
        self.session_time.setText(f"Session time: {sessionString}")

        # Calculate game time
        if CURRENT_SESSION.game_start != None:
            game_time = current_time - CURRENT_SESSION.game_start
            gameString = self.format_time(game_time)
            self.game_time.setText(f"Current game time: {gameString}")
        else:
            self.game_time.setText(f"Not in game")

        percentage_of_time_in_game_value  = 0
        total_time = CURRENT_SESSION.seconds_in_game+CURRENT_SESSION.seconds_out_of_game
        if total_time > 0:
            percentage_of_time_in_game_value = CURRENT_SESSION.seconds_in_game/(CURRENT_SESSION.seconds_in_game+CURRENT_SESSION.seconds_out_of_game)
            
        self.percentage_of_time_in_game.setText(f"Time in-game: {round(percentage_of_time_in_game_value * 100, 2)}")

    def format_time(self, elapsed_time : timedelta):
        hours, remainder = divmod(elapsed_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if hours > 0:
            formatted_string = f"{hours} hours, {minutes} minutes, {seconds} seconds"
        else:
            formatted_string = f"{minutes} minutes, {seconds} seconds"

        return formatted_string
    
    def on_update_app_state(self, state : State, changed_property):
        self.location_state.setText(f"{State()}")
        self.number_of_games.setText(f"Games joined: {CURRENT_SESSION.number_of_games}")


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
