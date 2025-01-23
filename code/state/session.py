from datetime import datetime
from dataclasses import dataclass, field
from typing import List
from pandas import Series
from event.event_manager import EventManager, EventType
from constants.contants import USER_PATH, DEFAULT_PROFILE, DEBUG_PATH
from utility.timer import Timer
import pandas as pd
import os
import re
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
    _items_in_session: List[dict] = field(default_factory=list, repr=False)
    _item_change_observers = []
    _items_debug_data = {}

    @property
    def items_in_session(self):
        return self._items_in_session

    def string_for_item(self, item):
        return item["Item"] +"_"+ item["Rarity"]
    
    def add_item(self, item, item_debug_data = None, manual = False):
        self._items_in_session.append(item);
        if item_debug_data:
            self._items_debug_data[self.string_for_item(item)] = item_debug_data
        add_item(item)
        for callback in self._item_change_observers:
            callback(item, "ADDED", manual)

    def remove_item(self, item, manual = True):
        # there will be a problem for multiple of same item, ditch the Series here maybe?
        if item in self._items_in_session:
            self._items_in_session.remove(item)
        if self.string_for_item(item) in self._items_debug_data != None:
            screenshot_path, text_lines = self._items_debug_data[self.string_for_item(item)]
            save_item_debug_data(screenshot_path, text_lines)
        remove_item(item)
        for callback in self._item_change_observers:
            callback(item, "REMOVED", manual)

    def subscribe_item_change(self, callback):
        self._item_change_observers.append(callback)

    def to_dict(self):
        return {
            "number_of_games": self.number_of_games,
            "session_start": self.session_start.isoformat(),  # Convert datetime to ISO string
            "items_in_session": [item["Item"] for item in self.items_in_session],
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
        items = data["items_in_session"]
        filtered_df = item_library[item_library['Item'].isin(items)]
        items_in_session = filtered_df.set_index('Item')['Rarity'].to_dict()

        # Return a new Session object with the deserialized data
        return cls(
            number_of_games=data["number_of_games"],
            session_start=session_start,
            _items_in_session=items_in_session,
            seconds_in_game=data["seconds_in_game"],
            seconds_out_of_game=data["seconds_out_of_game"],
        )

    def save_as_last_session(self):
        from state.application_state import ApplicationState
        last_session = self.to_dict()
        # save in profile sessions
        profile_path = f"{USER_PATH}{ApplicationState().current_profile.profile_name}/sessions/"
        os.makedirs(profile_path, exist_ok=True)
        file_path = f"{profile_path}{_sanitize_filename(self.session_start.isoformat())}.json"
        with open(file_path, "w") as file:
            json.dump(last_session, file, indent=4)
            
        # Open the file in write mode (it will be created if it doesn't exist)
        # save as last session and add profile name
        last_session["profile_name"] = ApplicationState().current_profile.profile_name
        with open(LAST_SESSION_PATH, "w") as file:
            json.dump(last_session, file, indent=4)


def add_item(entry):
    """
    Adds an item to the CSV file. If the item exists, increments its count.
    If not, adds it with a count of 1.
    """
    from state.application_state import ApplicationState
    profile_path = f"{USER_PATH}{ApplicationState().current_profile.profile_name}/"
    os.makedirs(profile_path, exist_ok=True)
    file_path = f"{profile_path}saved_items.csv"
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        # If the file doesn't exist, create an empty DataFrame with required columns
        df = pd.DataFrame(columns=["Item", "Rarity", "Count"])

    # Check if the entry exists in the DataFrame
    match = (df["Item"] == entry["Item"]) & (df["Rarity"] == entry["Rarity"])
    new_item = False
    if match.any():
        # If the entry exists, increment the count
        df.loc[match, "Count"] += 1
    else:
        # If the entry does not exist, add it with a count of 1
        new_row = {"Item": entry["Item"], "Rarity": entry["Rarity"], "Count": 1}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        EventManager().fire(EventType.BRAND_NEW_ITEM, entry)


    # Save the updated DataFrame back to the CSV file
    df.to_csv(file_path, index=False)
    return new_item

def remove_item(entry):
    """
    Removes an item from the CSV file. If the item's count reaches 0, removes the row.
    """
    from state.application_state import ApplicationState
    profile_path = f"{USER_PATH}{ApplicationState().current_profile.profile_name}/"
    os.makedirs(profile_path, exist_ok=True)
    file_path = f"{profile_path}saved_items.csv"
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("File not found. No items to remove.")
        return

    # Check if the entry exists in the DataFrame
    match = (df["Item"] == entry["Item"]) & (df["Rarity"] == entry["Rarity"])
    if match.any():
        # Decrease the count by 1
        df.loc[match, "Count"] -= 1

        # Remove rows where the count is now 0 or less
        df = df[df["Count"] > 0]

        # Save the updated DataFrame back to the CSV file
        df.to_csv(file_path, index=False)
    else:
        print("Item not found in the file.")

def handle_save_session():
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
    

def _sanitize_filename(filename):
    """
    Replaces invalid characters in a filename with underscores or other safe characters.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', filename)