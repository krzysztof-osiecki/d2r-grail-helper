from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import Qt
from state.application_state import ApplicationState
from state.screen_state import ScreenState
from utility.utility import format_time, format_time_float
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
        
        self.number_of_games = QLabel(f"Games joined: 0", self)
        self.number_of_games.setAlignment(Qt.AlignCenter)  
            
        self.percentage_of_time_in_game = QLabel(f"Time in-game: 0%", self)
        self.percentage_of_time_in_game.setAlignment(Qt.AlignCenter)  

        self.game_time = QLabel("Not in game...", self)
        self.game_time.setAlignment(Qt.AlignCenter)
        self.game_time.setWordWrap(True)
        self.game_time.setMaximumWidth(300)
        self.game_time.setTextFormat(Qt.RichText)

        grid_layout.addWidget(self.session_start)
        grid_layout.addWidget(self.session_time)
        grid_layout.addWidget(self.number_of_games)
        grid_layout.addWidget(self.game_time)
        grid_layout.addWidget(self.percentage_of_time_in_game)

        self.setLayout(grid_layout)
    
    def update(self):
        # i dont really like how it looks now, need to be polished
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
            
        self.percentage_of_time_in_game.setText(f"Time actively playing: {round(percentage_of_time_in_game_value * 100, 2)}%")
        self.number_of_games.setText(f"Games joined: {application_state.current_session.number_of_games}")

        current_time = datetime.now()
        # Calculate game time
        if application_state.current_session.game_timer != None:
            game_time = application_state.current_session.game_timer.get_total_time()
            paused_game_time = application_state.current_session.game_timer.get_paused_time()
            # if paused_game_time > 0:
                # self.game_time.setText(f"Game duration<br> <b>{format_time_float(game_time)}</b><br><br><br> Not in game for <br> {format_time_float(paused_game_time)}")
            # else:
            self.game_time.setText(f"Game duration<br> <b>{format_time_float(game_time)}</b>")
        else:
            self.game_time.setText(f"Not in game")