from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QLabel
from state.session import CURRENT_SESSION
from datetime import datetime
from utility.utility import format_time

class GameTab(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout(self)
        self.game_time = QLabel("Not in game...", self)
        grid_layout.addWidget(self.game_time)

    def update(self):
        current_time = datetime.now()
        # Calculate game time
        if CURRENT_SESSION.game_start != None:
            game_time = current_time - CURRENT_SESSION.game_start
            gameString = format_time(game_time)
            self.game_time.setText(f"Current game time: {gameString}")
        else:
            self.game_time.setText(f"Not in game")