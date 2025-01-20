import logging

from PySide6.QtWidgets import QApplication
from state.screen_state_observer import init_screen_state_observer
from screenshot.screenshot import init_screenshot_loop
from gui.main_window import MainWindow
from shortcuts.shortcuts import init_keyboard_shortcuts
from initialization.setup import initialize
from state.application_state import ApplicationState
from state.session import load_last_session, Session
from state.profile import load_profile

logger = logging.getLogger(__name__)

def main():
    initialize()
    init_screen_state_observer()
    init_keyboard_shortcuts()
    init_screenshot_loop()
    application_state = ApplicationState()
    # load and retain last session 
    # not sure if retaining is needed but i keep it for now
    application_state.last_session, last_profile = load_last_session()
    # create current session, maybe copy some data from last if needed
    application_state.current_session = Session()
    # load profile from last session
    application_state.current_profile = load_profile(last_profile)

    app = QApplication([]) 
    window = MainWindow()  
    window.show()          
    app.exec()              

if __name__ == "__main__":
    main()