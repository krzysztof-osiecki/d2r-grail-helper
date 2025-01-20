from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import Qt
from state.session import CURRENT_SESSION
from state.app import State
from utility.utility import format_time
from datetime import datetime

class MainTab(QWidget):
    def __init__(self):
        super().__init__()
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

        self.setLayout(grid_layout)
    
    def update(self):
        if State().in_game:
            CURRENT_SESSION.seconds_in_game += 1
        else:
            CURRENT_SESSION.seconds_out_of_game += 1

        # Get the current time and calculate the elapsed time
        current_time = datetime.now()
        
        # Calculate session time
        session_time = current_time - CURRENT_SESSION.session_start
        sessionString = format_time(session_time)
        self.session_time.setText(f"Session time: {sessionString}")

        percentage_of_time_in_game_value  = 0
        total_time = CURRENT_SESSION.seconds_in_game + CURRENT_SESSION.seconds_out_of_game
        if total_time > 0:
            percentage_of_time_in_game_value = CURRENT_SESSION.seconds_in_game/(CURRENT_SESSION.seconds_in_game+CURRENT_SESSION.seconds_out_of_game)
            
        self.percentage_of_time_in_game.setText(f"Time in-game: {round(percentage_of_time_in_game_value * 100, 2)}")
        self.location_state.setText(f"{State()}")
        self.number_of_games.setText(f"Games joined: {CURRENT_SESSION.number_of_games}")