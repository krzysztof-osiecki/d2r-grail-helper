import threading
import time
import pyautogui
import re
from constants.contants import RUNTIME_PATH
from recognition.location_recognition import recognize_location
from recognition.item_recognition import is_hovering_item
from ocr.ocr import get_text_from_image
from state.session import CURRENT_SESSION
from initialization.setup import ITEM_LIBRARY
import logging
from sound.play import play_item_search_started, play_item_found, play_item_not_found

import win32gui
import win32ui
import win32con
import win32api
from PIL import Image

logger = logging.getLogger(__name__)

screenshot_loop_counter = 0
screenshot_max_count = 10

def register_item():
    play_item_search_started()
    global screenshot_loop_counter, screenshot_max_count
    logger.debug("taking screenshot for item search")
    screenshot = pyautogui.screenshot()
    screenshot_path = RUNTIME_PATH + f"items/item_screenshot_{screenshot_loop_counter}.png"
    screenshot.save(screenshot_path)
    item_found, item_image_path = is_hovering_item(screenshot_path)
    if item_found:
        item_text = get_text_from_image(item_image_path)
        logger.warning(f"Text from item {item_text}")
        lines = item_text.splitlines()
        for item in lines:
            processed_item = preprocess_item(item)
            logger.warning(f"Looking for item {processed_item}")
            matching_rows = ITEM_LIBRARY["Item"].str.contains(processed_item, case=False)
            if len(processed_item) > 1 and matching_rows.any():
                for _, row in ITEM_LIBRARY[matching_rows].iterrows():
                    CURRENT_SESSION.items_saved.append(row)
                    CURRENT_SESSION.notify_item_change()
                    play_item_found()
                logger.warning(f"Found item: {item}")
                return
    play_item_not_found()



def take_screenshot():
    global screenshot_loop_counter, screenshot_max_count
    logger.debug("taking screenshot")
    screenshot = pyautogui.screenshot()
    screenshot_path = RUNTIME_PATH + f"screenshots/screenshot{screenshot_loop_counter}.png"
    screenshot.save(screenshot_path)
    screenshot_loop_counter = (screenshot_loop_counter + 1) % screenshot_max_count
    recognize_location(screenshot)
    logger.debug(f"screenshot taken successfully: {screenshot_path}")


# this is great but doesnt work for hardware accelerated windows :( maybe there is a way, don't see it now
def screenshot_window():
    window_title = "Diablo II: Resurrected"
    # window_title = "sound"
    """
    Capture a screenshot of the specified window by its title.
    
    :param window_title: Title of the window to capture.
    :return: PIL Image object of the screenshot.
    """
    # Find the window by title
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        raise Exception(f"Window with title '{window_title}' not found")

    # Get the window's dimensions
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    # Get the window's device context
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    # Create a compatible bitmap
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)

    # Copy the screen contents into the bitmap
    save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

    # Convert to a PIL Image
    bmpinfo = save_bitmap.GetInfo()
    bmpstr = save_bitmap.GetBitmapBits(True)
    img = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr,
        'raw',
        'BGRX',
        0,
        1
    )

    # Clean up resources
    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)

    return img

def preprocess_item(input_str):
    # Remove everything after and including the first bracket, including the space before it
    cleaned_str = re.sub(r'\s?\(.*\)', '', input_str)
    
    # Replace @ with O
    cleaned_str = cleaned_str.replace('@', 'O')
    
    # Trim leading and trailing spaces
    cleaned_str = cleaned_str.strip()
    
    return re.escape(cleaned_str)

def screenshot_loop():
    while True:
        take_screenshot()
        time.sleep(1)  # Wait for 1 second

def init_screenshot_loop():
    task_thread = threading.Thread(target=screenshot_loop, daemon=True)  # Set as daemon so it ends with the main program
    task_thread.start()