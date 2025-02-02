from PIL import Image
from skimage.metrics import structural_similarity as ssim
import numpy as np
from state.screen_state import ScreenState
from constants.contants import DATA_PATH, RUNTIME_PATH
import logging

logger = logging.getLogger(__name__)

LEFT_COLUMN_IMAGE_PATH = "left_column.jpg"
LEFT_COLUMN_SHADOWED_IMAGE_PATH = "left_column_shadowed.jpg"
LOADING_SCREEN_PATH = "loading_screen.jpg"
IN_GAME_PATH = "in_game.jpg"
LOCATION_SIMILARITY_THRESHOLD = 0.9
DEBUG_SCREEN_COUNTER = 0
MAX_DEBUG_SCREEN_COUNT = 0

# magic numbers in those functions are awful, fix them somehow

def recognize_location(screenshot, _):
    if on_character_screen(screenshot):
        logger.debug(f"we are on the character screen")
        return
    if on_character_screen_shadowed(screenshot):
        logger.debug(f"we are on the character screen with dialog")
        return
    if on_loading_screen(screenshot):
        logger.debug(f"we are on the loading screen")
        return
    if in_game(screenshot):
        logger.debug(f"we are in game")
        return

def in_game(screenshot):
    cropped_screenshot = screenshot.crop((373, 1292, 373 + 130, 1292 + 148))
    referenceImage = Image.open(f"{DATA_PATH}{IN_GAME_PATH}")
    similarity = calculate_similarity(cropped_screenshot, referenceImage)
    location_found = similarity > LOCATION_SIMILARITY_THRESHOLD
    ScreenState().in_game = location_found
    logger.debug(f"on_loading_screen: similarity factor {similarity}")
    return location_found

def on_loading_screen(screenshot):
    cropped_screenshot = screenshot.crop((1163, 1010, 1163 + 239, 1010 + 57))
    referenceImage = Image.open(f"{DATA_PATH}{LOADING_SCREEN_PATH}")
    similarity = calculate_similarity(cropped_screenshot, referenceImage,)
    location_found = similarity > LOCATION_SIMILARITY_THRESHOLD
    ScreenState().on_loading_screen = location_found
    logger.debug(f"on_loading_screen: similarity factor {similarity}")
    return location_found


def on_character_screen_shadowed(screenshot):
    cropped_screenshot = screenshot.crop((0, 0, 533, 973))
    referenceImage = Image.open(f"{DATA_PATH}{LEFT_COLUMN_SHADOWED_IMAGE_PATH}")
    similarity = calculate_similarity(cropped_screenshot, referenceImage)

    location_found = similarity > LOCATION_SIMILARITY_THRESHOLD
    ScreenState().on_character_screen = location_found
    logger.debug(f"check_character_screen shadowed: similarity factor {similarity}")
    return location_found

def on_character_screen(screenshot):
    cropped_screenshot = screenshot.crop((0, 0, 533, 973))
    referenceImage = Image.open(f"{DATA_PATH}{LEFT_COLUMN_IMAGE_PATH}")
    similarity = calculate_similarity(cropped_screenshot, referenceImage)

    location_found = similarity > LOCATION_SIMILARITY_THRESHOLD
    ScreenState().on_character_screen = location_found
    logger.debug(f"check_character_screen: similarity factor {similarity}")
    return location_found

def calculate_similarity(cropped_screenshot, left_column, save_debug = False):
    if save_debug:
        global DEBUG_SCREEN_COUNTER, MAX_DEBUG_SCREEN_COUNT
        cropped_screenshot.save(f"{RUNTIME_PATH}debug/cropped_screenshot{DEBUG_SCREEN_COUNTER}.png")
        DEBUG_SCREEN_COUNTER = (DEBUG_SCREEN_COUNTER + 1) % MAX_DEBUG_SCREEN_COUNT;

    # resize to make sure it matches
    resized_column = left_column.resize(cropped_screenshot.size)
    # Convert images to grayscale for comparison
    screenshot_gray = cropped_screenshot.convert("L")  # "L" mode is grayscale
    disk_image_gray = resized_column.convert("L")

    # Convert grayscale images to numpy arrays
    screenshot_array = np.array(screenshot_gray)
    disk_image_array = np.array(disk_image_gray)

    # Compute structural similarity
    similarity, _ = ssim(screenshot_array, disk_image_array, full=True)
    return similarity

# Version below searches based on opencv should work on all resolutions, but is slower and doesnt recognize details like paused game
# maybe come back to this lated
#
# def recognize_location(screenshot, screenshot_path):
#     if on_character_screen(screenshot_path):
#         logger.debug(f"we are on the character screen")
#         return
#     if on_character_screen_shadowed(screenshot_path):
#         logger.debug(f"we are on the character screen with dialog")
#         return
#     if on_loading_screen(screenshot_path):
#         logger.debug(f"we are on the loading screen")
#         return
#     if in_game(screenshot_path):
#         logger.debug(f"we are in game")
#         return

# def in_game(screenshot_path):
#     location_found = find_box_in_target(f"{DATA_PATH}{IN_GAME_PATH}", screenshot_path, 0.9)
#     ScreenState().in_game = location_found
#     return location_found

# def on_loading_screen(screenshot_path):
#     location_found = find_box_in_target(f"{DATA_PATH}{LOADING_SCREEN_PATH}", screenshot_path, 0.9)
#     ScreenState().on_loading_screen = location_found
#     return location_found


# def on_character_screen_shadowed(screenshot_path):
#     location_found = find_box_in_target(f"{DATA_PATH}{LEFT_COLUMN_SHADOWED_IMAGE_PATH}", screenshot_path, 0.9)
#     ScreenState().on_character_screen = location_found
#     return location_found

# def on_character_screen(screenshot_path):
#     location_found = find_box_in_target(f"{DATA_PATH}{LEFT_COLUMN_IMAGE_PATH}", screenshot_path, 0.9)
#     ScreenState().on_character_screen = location_found
#     return location_found