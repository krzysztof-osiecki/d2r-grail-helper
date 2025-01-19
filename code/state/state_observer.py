from state.app import State
import logging
from datetime import datetime
from state.session import CURRENT_SESSION

logger = logging.getLogger(__name__)

def init_state_observer():
    State().subscribe(on_state_change)


def on_state_change(state : State, changed_property):
    
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
                CURRENT_SESSION.number_of_games += 1;
                CURRENT_SESSION.game_start = datetime.now();
            else:
                CURRENT_SESSION.game_start = None
        case "on_loading_screen":
            if state.on_loading_screen:
                logging.debug(f"Showing dialog on character screen")
            else:
                logging.debug(f"Closed dialog on character screen")
        case _:
            logging.warning(f"unhandled state change {state}, {changed_property}")
