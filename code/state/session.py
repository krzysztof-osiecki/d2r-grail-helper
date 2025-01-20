from datetime import datetime
from dataclasses import dataclass, field
from typing import List
from pandas import Series

@dataclass
class Session():
    number_of_games: int = 0
    session_start: datetime = datetime.now()
    game_start: datetime = None
    items_saved: List[Series] = field(default_factory=list, repr=False)
    seconds_in_game: int = 0
    seconds_out_of_game: int = 0
    user_directory = "user_01/"
    _item_change_observers = []

    # should be done on append/remove from items_saved, dont see easy way to do this now except writing custom list
    def notify_item_change(self):
        """Notify all observers of state change"""
        for callback in self._item_change_observers:
            callback(self.items_saved)

    def subscribe_item_change(self, callback):
        self._item_change_observers.append(callback)

# todo load session from last remembered config
CURRENT_SESSION = Session()