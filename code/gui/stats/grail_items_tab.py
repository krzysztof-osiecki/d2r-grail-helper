from PySide6.QtWidgets import QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QAbstractItemView, QPushButton, QCheckBox
from PySide6.QtCore import Qt
from state.application_state import ApplicationState

class GrailItemsTab(QWidget):
    def __init__(self, saved_items_data, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.saved_items_data = saved_items_data
        self.all_items = True
        grid_layout = QGridLayout(self)
        self.checkbox = QCheckBox("Show All Items")
        self.checkbox.setChecked(self.all_items)  # Set initial state
        self.checkbox.stateChanged.connect(self.on_checkbox_toggled) 
        grid_layout.addWidget(self.checkbox)
        self.items_table = QTableWidget()
        self.items_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.load_data_into_table()
        grid_layout.addWidget(self.items_table)
        horizontal_header = self.items_table.horizontalHeader()
        horizontal_header.setMaximumHeight(40)
        horizontal_header.resizeSection(0, 20)
        horizontal_header.resizeSection(1, 20)
        vertical_header = self.items_table.verticalHeader()
        vertical_header.setVisible(False)

    def on_checkbox_toggled(self, state):
        """Slot to handle checkbox state changes."""
        self.all_items = state == 2  # 2 indicates checked, 0 indicates unchecked
        self.update()

    def update(self):
        self.load_data_into_table()

    def load_data_into_table(self):
        if self.all_items:
            application_state = ApplicationState()
            data_columns = ["Item", "Rarity"]  
            headers = ["", "", "Item", "Rarity", "Count"] 
            self.items_table.clear()
            self.items_table.setRowCount(len(application_state.item_library))  
            self.items_table.setColumnCount(len(headers)) 
            self.items_table.setHorizontalHeaderLabels(headers)
    
            for row in range(len(application_state.item_library)):
                dec_button = QPushButton("-")
                dec_button.setStyleSheet(
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
                dec_button.setCursor(Qt.PointingHandCursor)
                dec_button.clicked.connect(lambda checked, r=row: self.handle_dec_button_click(r))  
                self.items_table.setCellWidget(row, 0, dec_button)  
    
                inc_button = QPushButton("+")
                inc_button.setStyleSheet(
                    """
                    QPushButton {
                        color: green;
                        background-color: transparent;
                        border: none;
                        font-weight: bold;
                        border-radius: 5px;
                        padding: 2px 5px;
                    }
                    QPushButton:hover {
                        color: darkgreen;
                    }
                    """
                )
                inc_button.setCursor(Qt.PointingHandCursor)
                inc_button.clicked.connect(lambda checked, r=row: self.handle_inc_button_click(r)) 
                self.items_table.setCellWidget(row, 1, inc_button) 

                for col in range(len(data_columns)):
                    item = QTableWidgetItem(str(application_state.item_library.iloc[row, col])) 
                    self.items_table.setItem(row, col + 2, item) 
                
                count_for_item = self.get_count_for_item(row, application_state.item_library, self.saved_items_data)
                item = QTableWidgetItem(str(count_for_item))  
                self.items_table.setItem(row, len(headers)-1, item)  
        else:
            self.items_table.clear()
            self.items_table.setRowCount(len(self.saved_items_data)) 
            self.items_table.setColumnCount(len(self.saved_items_data.columns) + 2) 

            headers = ["", ""] + list(self.saved_items_data.columns) 
            self.items_table.setHorizontalHeaderLabels(headers)

            for row in range(len(self.saved_items_data)):
                dec_button = QPushButton("-")
                dec_button.setStyleSheet(
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
                dec_button.setCursor(Qt.PointingHandCursor)
                dec_button.clicked.connect(lambda checked, r=row: self.handle_dec_button_click(r))  
                self.items_table.setCellWidget(row, 0, dec_button)  
    
                inc_button = QPushButton("+")
                inc_button.setStyleSheet(
                    """
                    QPushButton {
                        color: green;
                        background-color: transparent;
                        border: none;
                        font-weight: bold;
                        border-radius: 5px;
                        padding: 2px 5px;
                    }
                    QPushButton:hover {
                        color: darkgreen;
                    }
                    """
                )
                inc_button.setCursor(Qt.PointingHandCursor)
                inc_button.clicked.connect(lambda checked, r=row: self.handle_inc_button_click(r))  
                self.items_table.setCellWidget(row, 1, inc_button) 

                # Populate the remaining columns with data from the DataFrame
                for col in range(len(self.saved_items_data.columns)):
                    item = QTableWidgetItem(str(self.saved_items_data.iloc[row, col]))  # Convert the data to string
                    self.items_table.setItem(row, col + 2, item)  # Shift by 1 for the button column
                

    def get_count_for_item(self, row_index, application_state, saved_items_data):
        # Step 1: Retrieve the value of "Item" column for the given row_index
        item_value = application_state.loc[row_index, 'Item']

        # Step 2: Search for the row in saved_items_data with the same "Item" value
        matching_row = saved_items_data[saved_items_data['Item'] == item_value]

        # Step 3: Return "Count" if row exists, otherwise return 0
        if not matching_row.empty:
            return matching_row.iloc[0]['Count']
        else:
            return 0

    def handle_inc_button_click(self, row):
        row_data = self.saved_items_data.iloc[row].to_dict()
        ApplicationState().current_session.add_item(row_data, manual=True)
        self.parent_window.update()


    def handle_dec_button_click(self, row):
        row_data = self.saved_items_data.iloc[row].to_dict()
        ApplicationState().current_session.remove_item(row_data)
        self.parent_window.update()
