from PySide6.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QAbstractItemView, QVBoxLayout
from PySide6.QtCore import Qt
from state.session import handle_save_session
from state.profile import handle_save_profile
from state.application_state import ApplicationState

class GrailItemsTab(QWidget):
    def __init__(self, saved_items_data):
        super().__init__()
        self.saved_items_data = saved_items_data
        grid_layout = QGridLayout(self)
        self.items_table = QTableWidget()
        self.items_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.load_data_into_table()
        grid_layout.addWidget(self.items_table)

    def load_data_into_table(self):
        # Set row count and column count
        self.items_table.setRowCount(len(self.saved_items_data))  # Number of rows based on the dataframe length
        self.items_table.setColumnCount(len(self.saved_items_data.columns))  # Number of columns based on the dataframe columns

        # Set horizontal header labels
        self.items_table.setHorizontalHeaderLabels(self.saved_items_data.columns)

        # Populate the table with data from the DataFrame
        for row in range(len(self.saved_items_data)):
            for col in range(len(self.saved_items_data.columns)):
                item = QTableWidgetItem(str(self.saved_items_data.iloc[row, col]))  # Convert the data to string
                self.items_table.setItem(row, col, item)