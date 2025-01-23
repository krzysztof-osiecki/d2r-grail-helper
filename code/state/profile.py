from dataclasses import dataclass
import json
import os
import logging
from constants.contants import USER_PATH, DEFAULT_PROFILE

logger = logging.getLogger(__name__)

@dataclass
class Profile():
    profile_name: str = DEFAULT_PROFILE

    def to_dict(self):
    # Convert to a dictionary with serialized data
        return {
            "profile_name": self.profile_name
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            profile_name=data["profile_name"]
        )
    
    def save_profile(self):
        USER_PROFILE_DIR =f"{USER_PATH}{self.profile_name}"
        os.makedirs(USER_PROFILE_DIR, exist_ok=True)
        USER_PROFILE_PATH = f"{USER_PROFILE_DIR}/profile.json"
        # Open the file in write mode (it will be created if it doesn't exist)
        with open(USER_PROFILE_PATH, "w") as file:
            # Serialize the object to a JSON string and write to the file
            json.dump(self.to_dict(), file, indent=4)
    
def handle_save_profile():
    from state.application_state import ApplicationState
    application_state = ApplicationState()
    application_state.current_profile.save_profile();

def load_profile(profile_name):
    USER_PROFILE_PATH = f"{USER_PATH}{profile_name}/profile.json"
    if not os.path.exists(USER_PROFILE_PATH):
        logger.debug("No last session file found, returning a default session.")
        return Profile(profile_name=profile_name)  # Return a default Session if the file is not found
    try:
        with open(USER_PROFILE_PATH, "r") as file:
            data = json.load(file)  # Load the JSON data from the file
            profile =  Profile.from_dict(data)  # Convert the data back into a Profile object
            return profile
    except (json.JSONDecodeError, KeyError) as e:
        logger.warning(f"Error reading the profile file: {e}. Returning a default object for given name.")
        return Profile(profile_name)  # Return a default Session if there is an error reading the file