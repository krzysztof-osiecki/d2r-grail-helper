from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from state.application_state import ApplicationState
from constants.contants import USER_PATH
import os
import json

class GrailStatsTab(QWidget):
    def __init__(self, saved_items_data):
        super().__init__()
        self.saved_items_data = saved_items_data

        grid_layout = QGridLayout(self)
        self.item_library = ApplicationState().item_library

        self.rarity_counts_for_owned = self.saved_items_data['Rarity'].value_counts()
        self.rarity_counts = self.item_library['Rarity'].value_counts()

        # Add rarities with zero items
        self.all_rarities = ['Unique', 'Set', 'Rune', 'Runeword']
        self.rarity_counts = self.rarity_counts.reindex(self.all_rarities, fill_value=0)
        self.rarity_counts_for_owned = self.rarity_counts_for_owned.reindex(self.all_rarities, fill_value=0)
        self.uniquesLabel = QLabel(f"<span style='color: #C38E4E;'>Uniques</span>: {self.rarity_counts_for_owned['Unique']}/{self.rarity_counts['Unique']}")
        self.setsLabel = QLabel(f"<span style='color: #3B9B3A;'>Sets</span>: {self.rarity_counts_for_owned['Set']}/{self.rarity_counts['Set']}")
        self.runesLabel = QLabel(f"<span style='color: #FFAA00;'>Runes</span>: {self.rarity_counts_for_owned['Rune']}/{self.rarity_counts['Rune']}")
        self.runewordsLabel = QLabel(f"<span style='color: #C7B377;'>Runewords</span>: {self.rarity_counts_for_owned['Runeword']}/{self.rarity_counts['Runeword']}")
        profile_sessions_path = f"{USER_PATH}{ApplicationState().current_profile.profile_name}/sessions/"
        total_values, max_values = process_session_files(profile_sessions_path)
        self.numberOfSessions = QLabel(f"""
You reached this place in {count_files_in_directory(profile_sessions_path)} sessions. {total_values["number_of_games"]} games joined, {total_values["seconds_in_game"]} seconds in game.
Longest sessions took {pretty_print_time(max_values["seconds_in_game"])} and the session with most games joined clocked at {max_values["number_of_games"]}.
Total time both ingame and out of game with helper launched was {pretty_print_time(total_values["seconds_in_game"] + total_values["seconds_out_of_game"])}
                                       """)
        self.label = QLabel("Your current grail collection stats")
        grid_layout.addWidget(self.label)
        grid_layout.addWidget(self.uniquesLabel)
        grid_layout.addWidget(self.setsLabel)
        grid_layout.addWidget(self.runesLabel)
        grid_layout.addWidget(self.runewordsLabel)
        grid_layout.addWidget(self.numberOfSessions)

    def update(self):
        self.rarity_counts_for_owned = self.saved_items_data['Rarity'].value_counts()
        self.rarity_counts = self.item_library['Rarity'].value_counts()
        self.rarity_counts = self.rarity_counts.reindex(self.all_rarities, fill_value=0)
        self.rarity_counts_for_owned = self.rarity_counts_for_owned.reindex(self.all_rarities, fill_value=0)
        self.uniquesLabel .setText(f"<span style='color: #C38E4E;'>Uniques</span>: {self.rarity_counts_for_owned['Unique']}/{self.rarity_counts['Unique']}")
        self.setsLabel .setText(f"<span style='color: #3B9B3A;'>Sets</span>: {self.rarity_counts_for_owned['Set']}/{self.rarity_counts['Set']}")
        self.runesLabel .setText(f"<span style='color: #FFAA00;'>Runes</span>: {self.rarity_counts_for_owned['Rune']}/{self.rarity_counts['Rune']}")
        self.runewordsLabel .setText(f"<span style='color: #C7B377;'>Runewords</span>: {self.rarity_counts_for_owned['Runeword']}/{self.rarity_counts['Runeword']}")

def count_files_in_directory(directory):
    """Counts the number of files in the given directory."""
    try:
        return sum(1 for entry in os.listdir(directory) if os.path.isfile(os.path.join(directory, entry)))
    except FileNotFoundError:
        print("Directory not found.")
        return 0
    
def process_session_files(directory):
    """Process JSON files in a directory to calculate total and maximum values for specific properties."""
    total_values = {"number_of_games": 0, "seconds_in_game": 0, "seconds_out_of_game": 0}
    max_values = {"number_of_games": 0, "seconds_in_game": 0, "seconds_out_of_game": 0}
    
    try:
        # Iterate through all files in the directory
        for entry in os.listdir(directory):
            file_path = os.path.join(directory, entry)
            # Process only .json files
            if os.path.isfile(file_path) and file_path.endswith('.json'):
                with open(file_path, 'r') as file:
                    try:
                        data = json.load(file)  # Load JSON data
                        # Update total values
                        for key in total_values:
                            if key in data:
                                total_values[key] += data[key]
                                # Update maximum values
                                max_values[key] = max(max_values[key], data[key])
                    except (json.JSONDecodeError, KeyError):
                        print(f"Skipping invalid or incomplete JSON file: {file_path}")
        
        return total_values, max_values
    except FileNotFoundError:
        print("Directory not found.")
        return total_values, max_values
    
def pretty_print_time(seconds):
    """Converts a number of seconds to a human-readable time format."""
    if seconds < 0:
        return "Invalid time"

    days, seconds = divmod(seconds, 86400)  # 86400 seconds in a day
    hours, seconds = divmod(seconds, 3600)  # 3600 seconds in an hour
    minutes, seconds = divmod(seconds, 60)  # 60 seconds in a minute

    if days > 0:
        return f"{days} days, {hours:02}:{minutes:02}:{seconds:02}"
    elif hours > 0:
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes:02}:{seconds:02}"
