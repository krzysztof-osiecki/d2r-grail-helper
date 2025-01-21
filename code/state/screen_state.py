from utility.timer import Timer

class ScreenState:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ScreenState, cls).__new__(cls, *args, **kwargs)
            cls._instance._observers = [] 
            cls._instance._on_character_screen = False
            cls._instance._on_loading_screen = False
            cls._instance._in_game = False
        return cls._instance

    def known_location(self):
        return self.on_character_screen or self.on_loading_screen or self.in_game

    @property
    def on_character_screen(self):
        return self._on_character_screen

    @on_character_screen.setter
    def on_character_screen(self, value):
        if self._on_character_screen != value:
            self._on_character_screen = value
            if value:
                self._on_loading_screen = False
                self._in_game = False
                # we enter character screen, so we know we are not in the game for sure
                # so we reset the game timer
                from state.application_state import ApplicationState
                application_state = ApplicationState()
                application_state.current_session.game_timer = None


    @property
    def on_loading_screen(self):
        return self._on_loading_screen

    @on_loading_screen.setter
    def on_loading_screen(self, value):
        if self._on_loading_screen != value:
            self._on_loading_screen = value
            if value:
                self._on_character_screen = False
                self._in_game = False

    @property
    def in_game(self):
        return self._in_game

    @in_game.setter
    def in_game(self, value):
        if self._in_game != value:
            self._in_game = value
            if value:
                self._on_character_screen = False
                self._on_loading_screen = False

            from state.application_state import ApplicationState
            application_state = ApplicationState()
            game_timer = application_state.current_session.game_timer
            # if are now in game are in game and dont have the timer so we are in a new game
            if value and game_timer == None:
                # reset character screen flag before next game
                self._was_on_character_screen = False
                # update session state, up the game counter and set game start to now
                application_state.current_session.number_of_games += 1
                game_timer = Timer()
                game_timer.start()
                application_state.current_session.game_timer = game_timer
            # we are in the same game we were resume the timer, if it was running nothing happens
            elif value:
                game_timer.resume()
            # if we are now not in game but have game timer we pause it we may not have it so need to check for existance
            else:
                if application_state.current_session.game_timer != None:
                    application_state.current_session.game_timer.pause()

    def __str__(self):
        if not self.known_location():
            return f"unkown location"
        if self.in_game:
            return f"in game"
        if self.on_character_screen:
            return f"character screen"
        if self.on_loading_screen:
            return f"loading"
        return "known but unmarked location"

    def __repr__(self):
        return self.__str__()