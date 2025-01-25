import keyboard
import threading
import pyautogui
from event.event_manager import EventManager, EventType
from constants.contants import RUNTIME_PATH
from screenshot.screenshot import search_for_item

def setup_global_shortcut():
    # This function will run in a separate thread to monitor the keyboard
    keyboard.add_hotkey("ctrl+shift+d", search_for_item)
    keyboard.add_hotkey("ctrl+shift+a", request_add_item)
    keyboard.wait()  # Keep listening for keyboard input

def request_add_item():
    EventManager().fire(EventType.REQUEST_ADD_ITEM, None)

def init_keyboard_shortcuts():
    shortcut_thread = threading.Thread(target=setup_global_shortcut, daemon=True)
    shortcut_thread.start()