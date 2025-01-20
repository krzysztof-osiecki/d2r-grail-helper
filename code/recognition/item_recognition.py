import cv2
from constants.contants import DATA_PATH, RUNTIME_PATH
import numpy as np
import logging
from ocr.ocr import get_text_from_image
from state.application_state import ApplicationState
import re

logger = logging.getLogger(__name__)

CROPPED_ITEM_INDEX = 0
MAX_CROPPED_ITEMS = 10

HOVER_ITEM_IMAGE_NAME = [
    "hover_item_drop.jpg",
    "hover_item_compare.jpg",
    "hover_item_unequip.jpg"
    "hover_item_move.jpg",
    ]
def recognize_item(screenshot_path, show_result_image = False):
    application_state = ApplicationState()
    item_found, item_image_path = find_item_box(screenshot_path, show_result_image)
    if not item_found: 
        return False
    
    item_text = get_text_from_image(item_image_path)
    logger.info(f"Text from item {item_text}")
    lines = item_text.splitlines()
    for item in lines:
        processed_item = preprocess_item_name(item)
        logger.info(f"Looking for item {processed_item}")
        matching_rows = application_state.item_library["Item"].str.contains(processed_item, case=False)
        if len(processed_item) > 1 and matching_rows.any():
            for _, row in application_state.item_library[matching_rows].iterrows():
                application_state.current_session.items_saved.append(row)
                application_state.current_session.notify_item_change()
                logger.warning(f"Found item: {item}")
                return True
    return False

def find_item_box(screenshot_path, show_result_image = False):
    global CROPPED_ITEM_INDEX, MAX_CROPPED_ITEMS
    for item in HOVER_ITEM_IMAGE_NAME:
        # Load the source image and template image
        source_image = cv2.imread(screenshot_path)  # The larger image
        template_image = cv2.imread(f"{DATA_PATH}hover_item_footers/{item}")  # The smaller image you're looking for

        # Convert images to grayscale (optional, but recommended for template matching)
        gray_source = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
        gray_template = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

        # Perform template matching using cv2.matchTemplate()
        result = cv2.matchTemplate(gray_source, gray_template, cv2.TM_CCOEFF_NORMED)
        # Initial threshold
        threshold = 0.8
        threshold_increment = 0.05  # Increment for increasing the threshold
        max_iterations = 10  # Maximum number of threshold increases to avoid infinite loop

        # Start with the initial threshold
        iteration = 0
        locations = []

        # Increase the threshold until only one match is found
        while len(locations) != 1 and iteration < max_iterations:
            # Find locations where the match score is greater than or equal to the threshold
            locations = np.where(result >= threshold)

            if len(locations) < 1:
                # nothing found
                break

            # Check if we found more than one match
            if len(locations[0]) > 1:
                # Increase the threshold
                threshold += threshold_increment
                iteration += 1
            else:
                # If exactly one match is found, break the loop
                break

        # Print result
        if len(locations[0]) == 1:
            print(f"Exactly one match found with threshold {threshold:.2f}")
            top_left = (locations[1][0], locations[0][0])  # Get top-left corner of the match
            bottom_right = (top_left[0] + gray_template.shape[1], top_left[1] + gray_template.shape[0])

            # extend the box a lot in the up direction as some items have very long descriptions
            # also a bit to the left and right, as the part we search for is in the middle but not full width
            top_left_extend = (locations[1][0] - 150, locations[0][0] - 1000) 
            bottom_right_extend  = (top_left[0] + gray_template.shape[1] + 150, top_left[1] + gray_template.shape[0])

            cropped_region = gray_source[max(top_left_extend[1],0):max(bottom_right_extend[1],0), top_left_extend[0]:bottom_right_extend[0]]
            output_path = f"{RUNTIME_PATH}items/cropped_item_{CROPPED_ITEM_INDEX}.jpg"
            CROPPED_ITEM_INDEX = (CROPPED_ITEM_INDEX + 1) % MAX_CROPPED_ITEMS
            cv2.imwrite(output_path, cropped_region)
            cv2.rectangle(source_image, top_left_extend, bottom_right_extend, (255, 255, 0), 2)

            if show_result_image:
                # Display the extended match
                cv2.imshow("Matched and Extended Image", source_image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

            return True, output_path
        else:
            logger.info(f"Unable to find exactly one match with item {item}.")

def preprocess_item_name(input_str):
    # Remove everything after and including the first bracket, including the space before it
    cleaned_str = re.sub(r'\s?\(.*\)', '', input_str)
    
    # Replace @ with O
    cleaned_str = cleaned_str.replace('@', 'O')
    
    # Trim leading and trailing spaces
    cleaned_str = cleaned_str.strip()
    
    return re.escape(cleaned_str)