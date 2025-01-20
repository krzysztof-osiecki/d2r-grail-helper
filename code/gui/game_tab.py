from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import Qt
from state.application_state import ApplicationState
from datetime import datetime
from utility.utility import format_time

class GameTab(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout(self)
        self.game_time = QLabel("Not in game...", self)
        self.game_time.setAlignment(Qt.AlignCenter)  
        grid_layout.addWidget(self.game_time)

    def update(self):
        application_state = ApplicationState()
        current_time = datetime.now()
        # Calculate game time
        if application_state.current_session.game_start != None:
            game_time = current_time - application_state.current_session.game_start
            gameString = format_time(game_time)
            self.game_time.setText(f"Current game time: {gameString}")
        else:
            self.game_time.setText(f"Not in game")