from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import Qt
from state.application_state import ApplicationState
from datetime import datetime
from utility.utility import format_time_float

class GameTab(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout(self)
        self.game_time = QLabel("Not in game...", self)
        self.game_time.setAlignment(Qt.AlignCenter)
        self.game_time.setWordWrap(True)
        self.game_time.setMaximumWidth(300)
        self.game_time.setTextFormat(Qt.RichText)
        grid_layout.addWidget(self.game_time)

    def update(self):
        application_state = ApplicationState()
        current_time = datetime.now()
        # Calculate game time
        if application_state.current_session.game_timer != None:
            game_time = application_state.current_session.game_timer.get_total_time()
            paused_game_time = application_state.current_session.game_timer.get_paused_time()
            if paused_game_time > 0:
                self.game_time.setText(f"Game duration<br> <b>{format_time_float(game_time)}</b><br><br><br> Not in game for <br> {format_time_float(paused_game_time)}")
            else:
                self.game_time.setText(f"Game duration<br> <b>{format_time_float(game_time)}</b>")
        else:
            self.game_time.setText(f"Not in game")