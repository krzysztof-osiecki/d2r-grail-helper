This is going to be D2R assistant for Holy Grail, and in general runs monitoring.
Currently the app expects the game to be run in 1440p, so the resolution is 2560x1440.
Item search is based on this resolution, to make it work with different, item search values would need to be adjusted, or simply written much better than current (quite stupid) approach.

Current features:
- item recognition and adding view in-game shortcut (not perfect)
- option to manualy add item from list
- game counting and in-game timer
- session timer
- recognized item popup (allowing removal of badly recognized)
- profiles with saved items and games counted
- monitoring grail collection (stats)

I don't normaly work with python, started with idea of using pipenv but didn't work for one of the libraries, so im just pip installing as i go.
Would like to make pipenv work at some point.

TODO and TOTHINK:

- rune recognition (check for particular letters swaps like het instead of hel, may add a few swaps to check)
- check if screenshot can ignore assistant window (see comment in screenshot.py method screenshot_window)