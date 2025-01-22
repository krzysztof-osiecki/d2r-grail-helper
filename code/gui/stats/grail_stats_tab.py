from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from state.session import handle_save_session
from state.profile import handle_save_profile
from state.application_state import ApplicationState

class GrailStatsTab(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout(self)
        label = QLabel("Calculate and present some stats here")
        grid_layout.addWidget(label)
