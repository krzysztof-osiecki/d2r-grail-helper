from PySide6.QtCore import QTimer, Qt, QSortFilterProxyModel
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QProgressBar, QComboBox, QLineEdit
from PySide6.QtGui import QStandardItemModel, QStandardItem
import pandas as pd
from pandas import Series
from state.application_state import ApplicationState
import logging
from PySide6.QtWidgets import (
    QWidget, QLineEdit, QListView, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QPushButton
)
from PySide6.QtCore import QStringListModel, Qt, Signal, QSortFilterProxyModel

from PySide6.QtWidgets import QWidget, QLineEdit, QListView, QVBoxLayout, QPushButton
from PySide6.QtCore import QStringListModel, Qt, Signal, QSortFilterProxyModel, QPoint, QItemSelectionModel
from PySide6.QtGui import QKeyEvent


logger = logging.getLogger(__name__)

class SelectItemNotification(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.dataset = ApplicationState().item_library

        # Set window flags to make it behave like a toast
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        # Apply styles
        self.setStyleSheet("background-color: #2E2E2E; border-radius: 10px;")

        # Layout for the content
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Create the QLabel with HTML formatted text
        label = QLabel(f"""You can choose the correct item""")
        label.setAlignment(Qt.AlignCenter)
        label.setMaximumHeight(30)
        label.setStyleSheet("color: white; font-size: 14px; padding: 0")
        layout.addWidget(label)

        options = []
        for item in self.dataset["Item"]:
          options.append(item)
        self.widget = Select2Widget(options, self)
        layout.addWidget(self.widget)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        layout.addLayout(buttons_layout)

        # Add green checkmark button
        btn_ok = QPushButton("✔")
        btn_ok.setStyleSheet(
            """
            QPushButton {
                background-color: green; 
                color: white; 
                font-size: 16px; 
                border: none; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #28a745;  /* Slightly lighter green */
            }
            """
        )
        btn_ok.clicked.connect(self.add_selected_item)
        buttons_layout.addWidget(btn_ok)

        # Add red X button
        btn_cancel = QPushButton("✖")
        btn_cancel.setStyleSheet(
            """
            QPushButton {
                background-color: red; 
                color: white; 
                font-size: 16px; 
                border: none; 
                padding: 10px; 
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #dc3545;  /* Slightly lighter red */
            }
            """
        )
        btn_cancel.clicked.connect(self.close)
        buttons_layout.addWidget(btn_cancel)

    def add_selected_item(self):
        item_from_library = self.dataset[self.dataset['Item'] == self.widget.selected_item]
        if not item_from_library.empty:  # Check if the filtered row exists
            item_dict = {
                "Item": self.widget.selected_item,
                "Rarity": item_from_library.iloc[0]["Rarity"],  # Access the 'Rarity' column
            }
            ApplicationState().current_session.add_item(item_dict, manual=True)
        else:
            logger.error("this should not happen, item was chosen from the list, it should be there!")
        self.close()

    def show_notification(self):
        """Display the toast notification in the top-right corner of the screen."""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        # Position it at the top-right corner (x = screen width - widget width, y = 0)
        widget_width = self.size().width()
        widget_height = self.size().height()
        x = screen_geometry.width() - widget_width - 150
        y = 20  # 20px padding from the top edge

        self.move(x, y)
        self.show()

class DropdownList(QListView):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set window flags to make it behave like a toast
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        self.setStyleSheet("border: 1px solid #333333;")
        self.current_index = -1

    def position_dropdown(self, target):
        line_edit_pos = target.mapToGlobal(target.rect().bottomLeft())
        # Position the popup directly below the QLineEdit
        self.move(line_edit_pos + QPoint(0, 5))  #

    def select_current_item(self):
        """Select the highlighted item."""
        if self.current_index >= 0:
            item = self.model().data(self.model().index(self.current_index, 0))
            self.parent().select_item_by_text(item)

class Select2Widget(QWidget):    
    def __init__(self, options, parent=None):
        super().__init__(parent)
        self.options = options
        self.selected_item = None
        self.dropdown_visible = False
        
        # Layouts
        self.main_layout = QVBoxLayout(self)
        
        # Search Field
        self.search_field = QLineEdit(self)
        self.search_field.setPlaceholderText("Search...")
        self.search_field.setMaximumHeight(30)
        self.search_field.textChanged.connect(self.filter_options)
        self.search_field.setFocusPolicy(Qt.StrongFocus)
        self.search_field.mousePressEvent = self.toggle_dropdown
        self.main_layout.addWidget(self.search_field)
        
       # Dropdown List View
        self.list_view = DropdownList(self)
        self.list_view.setVisible(False)  # Start hidden
        self.list_view.setMaximumHeight(150)
        self.list_view.setMaximumWidth(180)
        self.model = QStringListModel(self.options)
        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.list_view.setModel(self.proxy_model)
        self.list_view.clicked.connect(self.select_item)
    
    def showEvent(self, event):
        super().showEvent(event)
        self.activateWindow()
        self.search_field.setFocus()
        
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Up:
            if self.list_view.current_index > 0:
                self.list_view.current_index -= 1
                self.list_view.selectionModel().clearSelection()
                self.list_view.selectionModel().select(self.list_view.model().index(self.list_view.current_index, 0), QItemSelectionModel.Select)
        elif event.key() == Qt.Key_Down:
                self.list_view.current_index += 1
                self.list_view.selectionModel().clearSelection()
                self.list_view.selectionModel().select(self.list_view.model().index(self.list_view.current_index, 0), QItemSelectionModel.Select)
        elif event.key() == Qt.Key_Return:
            if self.dropdown_visible:
                self.list_view.select_current_item()
            else:
                self.parent().add_selected_item()
        elif event.key() == Qt.Key_Escape:
            self.close_dropdown();
        else:
            super().keyPressEvent(event)


    def close_dropdown(self):
        self.dropdown_visible = False
        self.list_view.setVisible(False)

    def toggle_dropdown(self, event):
        self.dropdown_visible = not self.dropdown_visible
        self.list_view.setVisible(self.dropdown_visible)
        self.list_view.position_dropdown(self.search_field)
        super().mousePressEvent(event)
    
    def filter_options(self, text):
        self.proxy_model.setFilterFixedString(text)
        if text and not self.dropdown_visible:
            self.list_view.setVisible(True)
            self.dropdown_visible = True
            self.list_view.position_dropdown(self.search_field)
    
    def select_item(self, index):
        item = self.proxy_model.data(index)
        self.selected_item = item
        self.list_view.setVisible(False)
        self.dropdown_visible = False
        self.search_field.textChanged.disconnect(self.filter_options)
        self.search_field.setText(item)
        self.search_field.textChanged.connect(self.filter_options)

    def select_item_by_text(self, item):
        self.selected_item = item
        self.list_view.setVisible(False)
        self.dropdown_visible = False
        self.search_field.textChanged.disconnect(self.filter_options)
        self.search_field.setText(item)
        self.search_field.textChanged.connect(self.filter_options)