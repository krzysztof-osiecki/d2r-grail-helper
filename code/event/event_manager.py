from enum import Enum
class EventType(str, Enum):
    REQUEST_ADD_ITEM = "REQUEST_ADD_ITEM"

class EventManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Ensure that only one instance of ApplicationState exists."""
        if cls._instance is None:
            print("Creating new EventManager instance")
            cls._instance = super(EventManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Initialize the application state."""
        if not hasattr(self, 'initialized'):  # Initialize only once
            self.initialized = True
            self._observers = {EventType.REQUEST_ADD_ITEM: []}

    def subscribe(self, event_type: EventType, callback):
        self._observers[event_type].append(callback)

    def fire(self, event_type: EventType, event_data):
        callbacks_for_type = self._observers[event_type]
        for callback in callbacks_for_type:
            callback(event_data)
