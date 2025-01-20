from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from state.session import handle_save_session
from state.profile import handle_save_profile
from state.application_state import ApplicationState

class SessionTab(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout(self)
        self.profile_label = QLabel("Current profile...", self)
        self.profile_label.setFixedHeight(30)
        self.profile_label.setAlignment(Qt.AlignCenter)  

        self.profile_name_input = QLineEdit(self)
        self.profile_name_input.setFixedHeight(30)
        self.profile_name_input.setPlaceholderText("enter user name...")
        self.profile_name_input.setText(ApplicationState().current_profile.profile_name)
        self.profile_name_input.setAlignment(Qt.AlignCenter)  

        self.save_session_button = QPushButton("Save session")
        self.save_session_button.clicked.connect(self.handle_save_session_button)

        grid_layout.addWidget(self.profile_label)
        grid_layout.addWidget(self.profile_name_input)
        grid_layout.addWidget(self.save_session_button)

        self.setLayout(grid_layout)

    def handle_save_session_button(self):
        ApplicationState().current_profile.profile_name = self.profile_name_input.text()
        handle_save_session()
        handle_save_profile()
