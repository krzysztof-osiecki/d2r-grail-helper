import keyboard
import threading
import pyautogui
from constants.contants import RUNTIME_PATH
from screenshot.screenshot import take_screenshot, search_for_item

def setup_global_shortcut():
    # This function will run in a separate thread to monitor the keyboard
    keyboard.add_hotkey("ctrl+shift+k", search_for_item)
    keyboard.wait()  # Keep listening for keyboard input

def init_keyboard_shortcuts():
    shortcut_thread = threading.Thread(target=setup_global_shortcut, daemon=True)
    shortcut_thread.start()