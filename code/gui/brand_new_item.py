from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QLabel, QPushButton, QHBoxLayout, QApplication
from pandas import Series
from PySide6.QtCore import Qt, QTimer

class BrandNewItemNotification(QWidget):
    def __init__(self, parent, item: dict):
        super().__init__(parent)
        self.parent = parent
        self.item = item
        # Set window flags to make it behave like a toast
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_ShowWithoutActivating)

        # Apply styles
        self.setStyleSheet("background-color: #2E2E2E; border-radius: 10px;")

        # Layout for the content
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        # Create a small progress bar to show time left
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedHeight(5)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(100)  # Start with full progress
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet("background-color: #444444; border-radius: 5px")
        layout.addWidget(self.progress_bar)

        # Determine the color based on the Rarity
        rarity = item["Rarity"]
        if rarity == "Set":
            color = "#3B9B3A"  # Dark green for Set items (approximation for Diablo 2 Resurrected)
        elif rarity == "Unique":
            color = "#C38E4E"  # Light brown/golden-brown for Unique items (approximation for Diablo 2 Resurrected)
        elif rarity == "Rune":
            color = "#FFAA00"
        elif rarity == "Runeword":
            color = "#C7B377"
        else:
            color = "black"  # Default color for other rarities

        # Create the QLabel with HTML formatted text
        label = QLabel(f"""<span style="color:{color}">{item["Item"]}</span> is a new item in your collection!""")

        label.setStyleSheet("color: white; font-size: 14px;")
        label.setWordWrap(True)
        layout.addWidget(label)


        # Auto-close the notification after a timeout
        self.timeout = 5000  # Timeout duration in milliseconds
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100) 
        # Initialize progress tracking
        self.remaining_time = self.timeout

    def update_progress(self):
        """Update the progress bar and close the toast when time is up."""
        self.remaining_time -= 100  # Decrease the time by 100ms
        progress = (self.remaining_time / self.timeout) * 100
        self.progress_bar.setValue(progress)

        if self.remaining_time <= 0:
            self.timer.stop()
            self.close()

    def show_notification(self):
        """Display the toast notification in the top-right corner of the screen."""
        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        # Position it at the top-right corner (x = screen width - widget width, y = 0)
        widget_width = self.size().width()
        widget_height = self.size().height()
        x = screen_geometry.width() - widget_width - 380 
        y = 20  # 20px padding from the top edge

        self.move(x, y)
        self.show()
