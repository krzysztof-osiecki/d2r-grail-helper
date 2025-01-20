This is going to be D2R assistant for Holy Grail, and in general runs monitoring.
Currently the app expects the game to be run in 1440p, so the resolution is 2560x1440.
Item search is based on this resolution, to make it work with different, item search values would need to be adjusted, or simply written much better than current (quite stupid) approach.

Current features:
- item recognition and adding view in-game shortcut (not perfect)
- game counting and in-game timer
- session timer
- session persisted items list

Expected features:
- monitoring grail collection
- persistance for items collection
- manual editing of items
- rune words monitoring

I don't normaly work with python, started with idea of using pipenv but didn't work for one of the libraries, so im just pip installing as i go.
Would like to make pipenv work at some point.

TODO and TOTHINK:
- make some nice toast notifying when actions are successful
- use them to show which item was recognized and allow user to tell if its wrong
- currently hiding game and showing again makes it count as new game (maybe reset game after seeing character screen)
- same with pressing ESC (darker filter makes area not recognized)
- and with long loading screen
- item hover can also cover the area checked for in-game
- check if screenshot can ignore assistant window (see comment in screenshot.py method screenshot_window)