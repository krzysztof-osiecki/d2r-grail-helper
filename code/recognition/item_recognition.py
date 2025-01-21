import cv2
from constants.contants import DATA_PATH, RUNTIME_PATH
import numpy as np
import logging
from ocr.ocr import get_text_from_image
from state.application_state import ApplicationState
from debug.debug_utility import save_item_debug_data
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz

logger = logging.getLogger(__name__)

CROPPED_ITEM_INDEX = 0
MAX_CROPPED_ITEMS = 20

HOVER_ITEM_IMAGE_NAME = [
    "hover_item_drop.jpg",
    "hover_item_compare.jpg",
    "hover_item_unequip.jpg",
    "hover_item_move.jpg",
    ]
def recognize_item(screenshot_path, show_result_image = False):
    application_state = ApplicationState()
    item_found, item_image_path = find_item_box(screenshot_path, show_result_image)
    if not item_found: 
        return False
    
    item_text = get_text_from_image(item_image_path)
    if item_text == None:
        logger.warning(f"Did not recognize any text from item, saving debug image!")
        save_item_debug_data(item_image_path, [])
        return False
    lines = item_text.splitlines()
    processed_lines = []
    for item in lines:
        processed_item = preprocess_item_name(item)
        processed_lines.append(processed_item)
        logger.debug(f"Looking for item {processed_item}")
        item_name = find_by_fuzzywuzzy_similarity(application_state.item_library, processed_item)
        if item_name != None:
            item_from_library = application_state.item_library[application_state.item_library['Item'] == item_name]
            if not item_from_library.empty:  # Check if the filtered row exists
                item_dict = {
                    "Item": item_name,
                    "Rarity": item_from_library.iloc[0]["Rarity"],  # Access the 'Rarity' column
                }
                item_debug_data = (item_image_path, processed_lines)
                application_state.current_session.add_item(item_dict, item_debug_data)
                return True
            else:
                logger.error("this should not happen, we found item but then it was not in dataframe!")
                return False
    save_item_debug_data(item_image_path, processed_lines)
    return False

def find_by_fuzzywuzzy_similarity(df, input_string, column="Item"):
    for item in df[column]:
        # sim1 = calculate_cosine_similarity(input_string.lower(), item.lower())
        # sim2 = jaccard_similarity(input_string.lower(), item.lower())
        # testing on few examples fuzzywuzzy seems best
        fuzzywuzzy_sim = fuzzywuzzy_similarity(input_string.lower(), item.lower())
        if fuzzywuzzy_sim > 90:
            print(item, input_string, fuzzywuzzy_sim)
            return item
    return None


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

            cropped_region = gray_source[max(top_left_extend[1],0):max(bottom_right_extend[1],0), max(top_left_extend[0],0):max(bottom_right_extend[0],0)]
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
        
        return False, None

def preprocess_item_name(input_str):
    # Remove everything after and including the first bracket, including the space before it
    cleaned_str = re.sub(r'\s?\(.*\)', '', input_str)
    # Replace @ with O
    cleaned_str = cleaned_str.replace('@', 'O')
    
    cleaned_string = re.sub(r"[^a-zA-Z']", "", cleaned_str)
    # Trim leading and trailing spaces
    cleaned_str = cleaned_str.strip()
    
    return re.escape(cleaned_str.lower())


# Function to calculate cosine similarity
def calculate_cosine_similarity(text1, text2):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return similarity[0][0]

# Function to calculate Jaccard similarity
def jaccard_similarity(text1, text2):
    words1 = set(text1.split())
    words2 = set(text2.split())
    intersection = len(words1 & words2)
    union = len(words1 | words2)
    return intersection / union

# Function to calculate fuzzywuzzy similarity
def fuzzywuzzy_similarity(text1, text2):
    return fuzz.ratio(text1, text2)