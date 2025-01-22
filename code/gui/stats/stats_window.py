from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel, QGridLayout, QTableWidget, QApplication, QTableWidgetItem, QTabWidget
from pandas import Series
from PySide6.QtCore import Qt, QTimer,  QCoreApplication
import os
from state.application_state import ApplicationState
from constants.contants import USER_PATH
import pandas as pd
from gui.stats.grail_items_tab import GrailItemsTab
from gui.stats.grail_stats_tab import GrailStatsTab

class StatsWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        saved_items_data = self.load_items_for_profile()

        self.setWindowFlags(Qt.Tool  | Qt.WindowStaysOnTopHint)
        application_state = ApplicationState()
        self.setWindowTitle(f"Grail stats for: {application_state.current_profile.profile_name}")

        self.stats_tab = GrailStatsTab()
        self.items_tab = GrailItemsTab(saved_items_data)

        tab_widget = QTabWidget(self)
        tab_widget.addTab(self.stats_tab, "Stats")
        tab_widget.addTab(self.items_tab, "Items")

        # Layout for the content
        layout = QGridLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(tab_widget)

    def load_items_for_profile(self):
        application_state = ApplicationState()
        profile_path = f"{USER_PATH}{application_state.current_profile.profile_name}/"
        os.makedirs(profile_path, exist_ok=True)
        saved_files_path = f"{profile_path}saved_items.csv"
        saved_items_data = pd.read_csv(saved_files_path)
        return saved_items_data

    def position_window(self):
        # Get the screen's available geometry (the area without taskbars, etc.)
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()
        
        # Calculate the center position
        screen_center = screen_geometry.center()
        
        # Get the window's size
        window_rect = self.frameGeometry()
        
        # Move the window to the center of the screen
        self.move(screen_center - window_rect.center())
        self.show()

