import logging
import pytesseract
import os
from constants.contants import RUNTIME_PATH, DATA_PATH
import pandas as pd

# load csv library of items
ITEM_LIBRARY = pd.read_csv(f"{DATA_PATH}item_library.csv")

def initialize():
    # create directories
    os.makedirs(RUNTIME_PATH + "log", exist_ok=True)
    os.makedirs(RUNTIME_PATH + "screenshots", exist_ok=True)
    os.makedirs(RUNTIME_PATH + "debug", exist_ok=True)
    os.makedirs(RUNTIME_PATH + "items", exist_ok=True)

    # setup logger
    logging.basicConfig(filename=RUNTIME_PATH + 'log/debug.log', encoding='utf-8', level=logging.INFO)

    # init pytesseract path
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    