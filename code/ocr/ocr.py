from PIL import Image
import pytesseract

def get_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang="eng")
    data = pytesseract.image_to_data(image)
    osd = pytesseract.image_to_osd(image)
    return text