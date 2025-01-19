import logging

from PySide6.QtWidgets import QApplication
from state.state_observer import init_state_observer
from state.app import State
from screenshot.screenshot import init_screenshot_loop
from gui.main_window import MainWindow
from shortcuts.shortcuts import init_keyboard_shortcuts
from initialization.setup import initialize

logger = logging.getLogger(__name__)
initialize()
init_state_observer()
init_keyboard_shortcuts()
init_screenshot_loop()

def main():
    app = QApplication([]) 
    window = MainWindow()  
    window.show()          
    app.exec()              

if __name__ == "__main__":
    main()