from PySide6.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem
from PySide6.QtCore import QTimer, QObject, Signal, QThread
from state.application_state import ApplicationState
class ItemsTab(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.current_session = ApplicationState().current_session
        grid_layout = QGridLayout(self)
        # Create the table widget
        self.items_table = QTableWidget()
        self.current_session.subscribe_item_change(self.update_items_table)
        grid_layout.addWidget(self.items_table)
        self.setLayout(grid_layout)

    def update_items_table(self, item, operation):
        if operation == "ADDED":
            self.main_window.item_add_worker.notify_with_last_added_item(item)

        self.items_table.setRowCount(len(self.current_session.items_saved))  # Set number of rows
        if len(self.current_session.items_saved) > 0:
            self.items_table.setColumnCount(len(self.current_session.items_saved[0].keys()))  # Set number of columns
            self.items_table.setHorizontalHeaderLabels(self.current_session.items_saved[0].keys())  # Set column headers

        # Populate the table with data
        for row_index, series in enumerate(self.current_session.items_saved):
            for col_index, (key, value) in enumerate(series.items()):
                self.items_table.setItem(row_index, col_index, QTableWidgetItem(str(value)))