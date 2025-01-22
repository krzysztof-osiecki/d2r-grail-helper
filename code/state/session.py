from datetime import datetime
from dataclasses import dataclass, field
from typing import List
from pandas import Series
from constants.contants import USER_PATH, DEFAULT_PROFILE, DEBUG_PATH
from utility.timer import Timer
import pandas as pd
import os
import json
import logging
from debug.debug_utility import save_item_debug_data


logger = logging.getLogger(__name__)

LAST_SESSION_PATH = f"{USER_PATH}last_session.json"

@dataclass
class Session():
    number_of_games: int = 0
    session_start: datetime = datetime.now()
    game_timer: Timer = None
    seconds_in_game: int = 0
    seconds_out_of_game: int = 0
    _items_saved: List[dict] = field(default_factory=list, repr=False)
    _item_change_observers = []
    _items_debug_data = {}

    @property
    def items_saved(self):
        return self._items_saved

    def string_for_item(self, item):
        return item["Item"] +"_"+ item["Rarity"]
    
    def add_item(self, item, item_debug_data = None, manual = False):
        self._items_saved.append(item);
        if item_debug_data:
            self._items_debug_data[self.string_for_item(item)] = item_debug_data
        for callback in self._item_change_observers:
            callback(item, "ADDED", manual)

    def remove_item(self, item, manual = True):
        # there will be a problem for multiple of same item, ditch the Series here maybe?
        self._items_saved.remove(item)
        if self.string_for_item(item) in self._items_debug_data != None:
            screenshot_path, text_lines = self._items_debug_data[self.string_for_item(item)]
            save_item_debug_data(screenshot_path, text_lines)

        for callback in self._item_change_observers:
            callback(item, "REMOVED", manual)

    def subscribe_item_change(self, callback):
        self._item_change_observers.append(callback)

    def to_dict(self):
        return {
            "number_of_games": self.number_of_games,
            "session_start": self.session_start.isoformat(),  # Convert datetime to ISO string
            "items_saved": [item["Item"] for item in self.items_saved],
            "seconds_in_game": self.seconds_in_game,
            "seconds_out_of_game": self.seconds_out_of_game
        }
    
    @classmethod
    def from_dict(cls, data):
        """Convert a dictionary back into a Session object."""
        # Deserialize datetime fields from ISO format strings
        session_start = datetime.fromisoformat(data["session_start"])
        from state.application_state import ApplicationState
        item_library = ApplicationState().item_library
        # Convert the list of dictionaries back into Series objects
        items = data["items_saved"]
        filtered_df = item_library[item_library['Item'].isin(items)]
        items_saved = filtered_df.set_index('Item')['Rarity'].to_dict()

        # Return a new Session object with the deserialized data
        return cls(
            number_of_games=data["number_of_games"],
            session_start=session_start,
            _items_saved=items_saved,
            seconds_in_game=data["seconds_in_game"],
            seconds_out_of_game=data["seconds_out_of_game"],
        )

    def save_as_last_session(self):
        # Open the file in write mode (it will be created if it doesn't exist)
        with open(LAST_SESSION_PATH, "w") as file:
            # Serialize the object to a JSON string and write to the file
            last_session = self.to_dict()
            from state.application_state import ApplicationState
            last_session["profile_name"] = ApplicationState().current_profile.profile_name
            json.dump(last_session, file, indent=4)

def handle_save_session():
    _save_items()

    from state.application_state import ApplicationState
    application_state = ApplicationState()
    application_state.current_session.save_as_last_session();

def load_last_session():
    if not os.path.exists(LAST_SESSION_PATH):
        logger.debug("No last session file found, returning a default session.")
        return Session(), DEFAULT_PROFILE  # Return a default Session if the file is not found
    try:
        with open(LAST_SESSION_PATH, "r") as file:
            data = json.load(file)  # Load the JSON data from the file
            return Session.from_dict(data), data["profile_name"]  # Convert the data back into a Session object
    except (json.JSONDecodeError, KeyError) as e:
        logger.warning(f"Error reading the session file: {e}. Returning a default session.")
        return Session(), DEFAULT_PROFILE  # Return a default Session if there is an error reading the file
    
def _save_items():
    # analyze if it is needed to write whole series of item as this data is in item library anyway
    # might be more usefull if i would read some item stats or etherial state
    from state.application_state import ApplicationState
    application_state = ApplicationState()
    
    # Create DataFrame from saved items
    df = pd.DataFrame(application_state.current_session.items_saved)
    
    # Define the directory and file path
    profile_path = f"{USER_PATH}{application_state.current_profile.profile_name}/"
    os.makedirs(profile_path, exist_ok=True)
    saved_files_path = f"{profile_path}saved_items.csv"
    
    if os.path.exists(saved_files_path):
        with open(saved_files_path, 'r') as file:
            file_contents = file.read().strip()  # Remove leading/trailing whitespace
            if file_contents:  # If the file contains non-whitespace text
                df.to_csv(saved_files_path, mode='a', header=False, index=False)
            else:
                df.to_csv(saved_files_path, mode='w', header=True, index=False)
    else :
        df.to_csv(saved_files_path, mode='w', header=True, index=False)
    
        
