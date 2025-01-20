from state.session import Session
from state.profile import Profile
from pandas import DataFrame

class ApplicationState:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Ensure that only one instance of ApplicationState exists."""
        if cls._instance is None:
            print("Creating new ApplicationState instance")
            cls._instance = super(ApplicationState, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Initialize the application state."""
        if not hasattr(self, 'initialized'):  # Initialize only once
            self.initialized = True
            self._current_session = None
            self._last_session = None
            self._item_library = None

    @property
    def item_library(self):
        return self._item_library

    @item_library.setter
    def item_library(self, value: DataFrame):
        if isinstance(value, DataFrame):
            self._item_library = value
        else:
            raise ValueError("item_library must be a DataFrame.")

    @property
    def current_session(self):
        return self._current_session

    @current_session.setter
    def current_session(self, value: Session):
        if isinstance(value, Session):
            self._current_session = value
        else:
            raise ValueError("current_session must be a Session.")

    @property
    def current_profile(self):
        return self._current_profile

    @current_profile.setter
    def current_profile(self, value: Profile):
        if isinstance(value, Profile):
            self._current_profile = value
        else:
            raise ValueError("current_profile must be a Profile.")
        
    @property
    def last_session(self):
        return self._last_session

    @last_session.setter
    def last_session(self, value: Session):
        if isinstance(value, Session):
            self._last_session = value
        else:
            raise ValueError("last_session must be a Session.")