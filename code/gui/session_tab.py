from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from state.session import CURRENT_SESSION
from constants.contants import USER_PATH
import pandas as pd
import os

class SessionTab(QWidget):
    def __init__(self):
        super().__init__()

        grid_layout = QGridLayout(self)
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Enter some text here...")
        self.text_input.setAlignment(Qt.AlignCenter)  

        self.save_session_button = QPushButton("Save session")
        self.save_session_button.clicked.connect(self.save_session)

        grid_layout.addWidget(self.text_input)
        grid_layout.addWidget(self.save_session_button)

        self.setLayout(grid_layout)


    def save_session(self):
        """
        Save a list of pandas Series to a CSV file.
        If the file exists, append the data; otherwise, create the file with a header.

        :param series_list: List of pandas Series to save
        :param file_path: Path to the CSV file
        """
        # Convert the list of Series to a DataFrame
        df = pd.DataFrame(CURRENT_SESSION.items_saved)

        os.makedirs(f"{USER_PATH}{CURRENT_SESSION.user_directory}", exist_ok=True)
        saved_files_path = f"{USER_PATH}{CURRENT_SESSION.user_directory}saved_items.csv"

         # Check if the file exists
        if os.path.exists(saved_files_path):
            # Append to the file without writing the header
            df.to_csv(saved_files_path, mode='a', header=False, index=False)
        else:
            # Create a new file with a header
            df.to_csv(saved_files_path, mode='w', header=True, index=False)