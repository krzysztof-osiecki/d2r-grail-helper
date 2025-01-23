from PySide6.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QAbstractItemView, QPushButton
from PySide6.QtCore import Qt
from state.application_state import ApplicationState

class GrailItemsTab(QWidget):
    def __init__(self, saved_items_data, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.saved_items_data = saved_items_data
        grid_layout = QGridLayout(self)
        self.items_table = QTableWidget()
        self.items_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.load_data_into_table()
        grid_layout.addWidget(self.items_table)
        horizontal_header = self.items_table.horizontalHeader()
        horizontal_header.setMaximumHeight(40)
        horizontal_header.resizeSection(0, 20)
        vertical_header = self.items_table.verticalHeader()
        vertical_header.setVisible(False)


    def update(self):
        self.load_data_into_table()

    def load_data_into_table(self):
        # Set row count and column count (adding 1 extra column for buttons)
        self.items_table.setRowCount(len(self.saved_items_data))  # Number of rows based on the DataFrame length
        self.items_table.setColumnCount(len(self.saved_items_data.columns) + 1)  # Add 1 for the new button column

        # Set horizontal header labels (adding a header for the button column)
        headers = [""] + list(self.saved_items_data.columns)  # Add "Action" as the first column header
        self.items_table.setHorizontalHeaderLabels(headers)

        # Populate the table with data
        for row in range(len(self.saved_items_data)):
            # Add the QPushButton in the first column
            button = QPushButton("-")
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
            button.clicked.connect(lambda checked, r=row: self.handle_button_click(r))  # Connect to a method with the row index
            self.items_table.setCellWidget(row, 0, button)  # Place the button in the first column of the current row

            # Populate the remaining columns with data from the DataFrame
            for col in range(len(self.saved_items_data.columns)):
                item = QTableWidgetItem(str(self.saved_items_data.iloc[row, col]))  # Convert the data to string
                self.items_table.setItem(row, col + 1, item)  # Shift by 1 for the button column

    def handle_button_click(self, row):
        row_data = self.saved_items_data.iloc[row].to_dict()
        ApplicationState().current_session.remove_item(row_data)
        self.parent_window.update()
