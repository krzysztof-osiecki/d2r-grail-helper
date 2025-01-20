from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton

class SessionTab(QWidget):
    def __init__(self):
        super().__init__()

        grid_layout = QGridLayout(self)
        # Create the table widget
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Enter some text here...")

        self.save_session_button = QPushButton("Save session")
        self.save_session_button.clicked.connect(self.save_session)
        grid_layout.addWidget(self.text_input)
        grid_layout.addWidget(self.save_session_button)

        self.setLayout(grid_layout)

    def save_session(self):
        print("save session clicked")