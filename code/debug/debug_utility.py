import shutil
import uuid
from constants.contants import DEBUG_PATH

def save_item_debug_data(screenshot_path, text_lines):
    random_uuid = uuid.uuid4()
    destination_path = f"{DEBUG_PATH}{random_uuid.hex}"
    shutil.move(screenshot_path, destination_path+".jpg")       
     # Step 2: Write the array of lines to the new file
    with open(destination_path +".txt", 'w') as file:
        for line in text_lines:
            file.write(line + '\n')  # Add newline to each line