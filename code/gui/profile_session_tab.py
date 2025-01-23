from PySide6.QtWidgets import (
    QWidget,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QLineEdit,
    QAbstractItemView,
    QLabel
)
from PySide6.QtCore import Qt
from functools import partial
from state.application_state import ApplicationState
from state.profile import handle_save_profile


class ProfileSessionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.current_session = ApplicationState().current_session

        grid_layout = QGridLayout(self)
        self.items_table = QTableWidget()
        
        self.items_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.profile_name_input = QLineEdit(self)
        self.profile_name_input.setFixedHeight(30)
        self.profile_name_input.setPlaceholderText("enter user name...")
        self.profile_name_input.setText(ApplicationState().current_profile.profile_name)
        self.profile_name_input.setAlignment(Qt.AlignCenter)  

        self.create_profile_button = QPushButton("Set profile")
        self.create_profile_button.clicked.connect(self.handle_create_profile_button)

        grid_layout.addWidget(self.profile_name_input, 0, 0, 1, 2)
        grid_layout.addWidget(self.create_profile_button, 0, 2, 1, 1)
        grid_layout.addWidget(self.items_table, 1, 0, 1, 3)
        self.setLayout(grid_layout)

    def update_items_table(self):

        # Set up rows and columns
        row_count = len(self.current_session.items_in_session)
        self.items_table.setRowCount(row_count)  # Set number of rows

        if row_count > 0:
            # Add the "Actions" column at the beginning
            col_headers = [""] + list(self.current_session.items_in_session[0].keys())
            self.items_table.setColumnCount(len(col_headers))  # Add one column for actions
            self.items_table.setHorizontalHeaderLabels(col_headers)

        horizontal_header = self.items_table.horizontalHeader()
        horizontal_header.setMaximumHeight(40)
        horizontal_header.resizeSection(0, 20)
        vertical_header = self.items_table.verticalHeader()
        vertical_header.setVisible(False)

        # Populate the table with data and add buttons
        for row_index, series in enumerate(self.current_session.items_in_session):
            # Add the remove button to the "Actions" column (first column)
            button = QPushButton("X")
            # button.setMaximumWidth(20)
            button.setStyleSheet(
                """
                QPushButton {
                    color: red;
                    background-color: transparent;
                    border: none;
                    font-weight: bold;
                    border-radius: 5px;
                    padding: 2px 5px;
                }
                QPushButton:hover {
                    color: darkred;
                }
                """
            )
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(partial(self.remove_row, row_index))

            self.items_table.setCellWidget(row_index, 0, button)  # Set the button in the first column

            # Populate other columns with item data
            for col_index, (key, value) in enumerate(series.items()):
                self.items_table.setItem(row_index, col_index + 1, QTableWidgetItem(str(value)))  # +1 because "Actions" is at index 0

    def remove_row(self, row_index):
        # Remove the item from the ApplicationState
        if 0 <= row_index < len(self.current_session.items_in_session):
            removed_item = self.current_session.items_in_session[row_index]
            ApplicationState().current_session.remove_item(removed_item)

    def handle_create_profile_button(self):
        ApplicationState().current_profile.profile_name = self.profile_name_input.text()
        handle_save_profile()
