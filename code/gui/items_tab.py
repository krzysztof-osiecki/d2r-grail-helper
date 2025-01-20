from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
from state.session import CURRENT_SESSION

class ItemsTab(QWidget):
    def __init__(self):
        super().__init__()
        grid_layout = QGridLayout(self)
        # Create the table widget
        self.items_table = QTableWidget()
        CURRENT_SESSION.subscribe_item_change(self.update_items_table)
        self.update_items_table(CURRENT_SESSION.items_saved)
        grid_layout.addWidget(self.items_table)
        self.setLayout(grid_layout)

    def update_items_table(self, items_saved):
        if len(items_saved) > 0:
            self.items_table.setRowCount(len(items_saved))  # Set number of rows
            self.items_table.setColumnCount(len(items_saved[0].index))  # Set number of columns
            self.items_table.setHorizontalHeaderLabels(items_saved[0].index.tolist())  # Set column headers

        # Populate the table with data
        for row_index, series in enumerate(items_saved):
            for col_index, (key, value) in enumerate(series.items()):
                self.items_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))