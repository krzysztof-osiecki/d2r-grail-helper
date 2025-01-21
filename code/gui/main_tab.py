from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import Qt
from state.application_state import ApplicationState
from state.screen_state import ScreenState
from utility.utility import format_time
from datetime import datetime

class MainTab(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout(self)
        application_state = ApplicationState()
        self.session_start = QLabel(f"Session started {application_state.current_session.session_start.strftime("%Y-%m-%d %H:%M:%S")}", self)
        self.session_start.setAlignment(Qt.AlignCenter)  

        self.session_time = QLabel("Timer is starting...", self)
        self.session_time.setAlignment(Qt.AlignCenter) 

        self.screen_state = QLabel(f"{ScreenState()}", self)
        self.screen_state.setAlignment(Qt.AlignCenter) 

        self.number_of_games = QLabel(f"Games joined: 0", self)
        self.number_of_games.setAlignment(Qt.AlignCenter)  
            
        self.percentage_of_time_in_game = QLabel(f"Time in-game: 0%", self)
        self.percentage_of_time_in_game.setAlignment(Qt.AlignCenter)  

        grid_layout.addWidget(self.session_start)
        grid_layout.addWidget(self.session_time)
        grid_layout.addWidget(self.screen_state)
        grid_layout.addWidget(self.number_of_games)
        grid_layout.addWidget(self.percentage_of_time_in_game)

        self.setLayout(grid_layout)
    
    def update(self):
        application_state = ApplicationState()
        if ScreenState().in_game:
            application_state.current_session.seconds_in_game += 1
        else:
            application_state.current_session.seconds_out_of_game += 1

        # Get the current time and calculate the elapsed time
        current_time = datetime.now()
        
        # Calculate session time
        session_time = current_time - application_state.current_session.session_start
        sessionString = format_time(session_time)
        self.session_time.setText(f"Session time: {sessionString}")

        percentage_of_time_in_game_value  = 0
        total_time = application_state.current_session.seconds_in_game + application_state.current_session.seconds_out_of_game
        if total_time > 0:
            percentage_of_time_in_game_value = application_state.current_session.seconds_in_game/(application_state.current_session.seconds_in_game+application_state.current_session.seconds_out_of_game)
            
        self.percentage_of_time_in_game.setText(f"Time in-game: {round(percentage_of_time_in_game_value * 100, 2)}%")
        self.screen_state.setText(f"{ScreenState()}")
        self.number_of_games.setText(f"Games joined: {application_state.current_session.number_of_games}")