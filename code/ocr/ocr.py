from PIL import Image
import pytesseract
from constants.contants import DATA_PATH

def get_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang="eng", config=f'--user-words {f"{DATA_PATH}recognizable_items.csv"}')
    return text