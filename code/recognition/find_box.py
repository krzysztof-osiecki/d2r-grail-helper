import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

# separated this in hopes of changing location logic to this, but doesnt seem to be working now
# this separation is fine anyway (except maybe 5 returned values) so i leave like this

def find_box_in_target(box_path, target_path, initial_threshold = 0.8):
    source_image = cv2.imread(target_path)  # The larger image
    template_image = cv2.imread(box_path)  # The smaller image you're looking for
    # Convert images to grayscale (optional, but recommended for template matching)
    gray_source = cv2.cvtColor(source_image, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)
    # Perform template matching using cv2.matchTemplate()
    result = cv2.matchTemplate(gray_source, gray_template, cv2.TM_CCOEFF_NORMED)
    # Initial threshold
    threshold = initial_threshold
    threshold_increment = 0.05  # Increment for increasing the threshold
    max_iterations = 10  # Maximum number of threshold increases to avoid infinite loop

    # Start with the initial threshold
    iteration = 0
    locations = []

    # Increase the threshold until only one match is found
    while iteration < max_iterations:
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
        elif len(locations[0]) == 1:
            # If exactly one match is found, break the loop
            logger.debug(f"Exactly one match found with threshold {threshold:.2f}")
            break
        else:
            logger.debug(f"Nothing found")
            # none is found
            break

    return len(locations[0])==1, locations, gray_source, gray_template, source_image