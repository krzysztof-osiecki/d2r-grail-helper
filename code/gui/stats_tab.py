from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton
from PySide6.QtCore import Qt
from state.application_state import ApplicationState
from state.screen_state import ScreenState
from utility.utility import format_time
from datetime import datetime
from gui.stats.stats_window import StatsWindow

class StatsTab(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout(self)
        show_grail_stats_window_button = QPushButton("Show grail stats window")
        show_grail_stats_window_button.clicked.connect(self.show_grail_stats_window)
        grid_layout.addWidget(show_grail_stats_window_button)
        self.setLayout(grid_layout)

    def show_grail_stats_window(self):
        stats_window = StatsWindow(self)
        stats_window.position_window()