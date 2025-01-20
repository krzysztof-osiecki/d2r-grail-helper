from state.screen_state import ScreenState
import logging
from datetime import datetime
from state.application_state import ApplicationState

logger = logging.getLogger(__name__)

def init_screen_state_observer():
    ScreenState().subscribe(on_screen_state_change)


def on_screen_state_change(state : ScreenState, changed_property):
    application_state = ApplicationState()
    match changed_property:
        case "on_character_screen" :
            if state.on_character_screen:
                logging.debug(f"Entered character screen")
            else:
                logging.debug(f"Left character screen")
        case "on_character_screen_with_dialog":
            if state.on_character_screen_with_dialog:
                logging.debug(f"Showing dialog on character screen")
            else:
                logging.debug(f"Closed dialog on character screen")
        case "in_game":
            if state.in_game:
                application_state.current_session.number_of_games += 1;
                application_state.current_session.game_start = datetime.now();
            else:
                application_state.current_session.game_start = None
        case "on_loading_screen":
            if state.on_loading_screen:
                logging.debug(f"Showing dialog on character screen")
            else:
                logging.debug(f"Closed dialog on character screen")
        case _:
            logging.warning(f"unhandled state change {state}, {changed_property}")
