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