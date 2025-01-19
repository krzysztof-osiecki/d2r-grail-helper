class State:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(State, cls).__new__(cls, *args, **kwargs)
            cls._instance._observers = [] 
            cls._instance._on_character_screen = False
            cls._instance._on_character_screen_with_dialog = False
            cls._instance._on_loading_screen = False
            cls._instance._in_game = False
        return cls._instance

    def subscribe(self, callback):
        """Subscribe an observer callback to state changes"""
        self._observers.append(callback)

    def _notify(self, property_name):
        """Notify all observers of state change"""
        for callback in self._observers:
            callback(self, property_name)

    def known_location(self):
        return self.on_character_screen or self.on_character_screen_with_dialog or self.on_loading_screen or self.in_game

    @property
    def on_character_screen(self):
        return self._on_character_screen

    @on_character_screen.setter
    def on_character_screen(self, value):
        if self._on_character_screen != value:
            self._on_character_screen = value
            self._notify("on_character_screen")

    @property
    def on_character_screen_with_dialog(self):
        return self._on_character_screen_with_dialog

    @on_character_screen_with_dialog.setter
    def on_character_screen_with_dialog(self, value):
        if self._on_character_screen_with_dialog != value:
            self._on_character_screen_with_dialog = value
            self._notify("on_character_screen_with_dialog")

    @property
    def on_loading_screen(self):
        return self._on_loading_screen

    @on_loading_screen.setter
    def on_loading_screen(self, value):
        if self._on_loading_screen != value:
            self._on_loading_screen = value
            self._notify("on_loading_screen")

    @property
    def in_game(self):
        return self._in_game

    @in_game.setter
    def in_game(self, value):
        if self._in_game != value:
            self._in_game = value
            self._notify("in_game")

    def __str__(self):
        if not self.known_location():
            return f"unkown location"
        if self.in_game:
            return f"in game"
        if self.on_character_screen:
            return f"character screen"
        if self.on_character_screen_with_dialog:
            return f"character screen with options"
        if self.on_loading_screen:
            return f"loading"
        return "known but unmarked location"

    def __repr__(self):
        return self.__str__()