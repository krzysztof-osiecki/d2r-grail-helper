import pygame
from constants.contants import DATA_PATH

def play_item_search_started():
    # Initialize pygame mixer
    pygame.mixer.init()
    # Load the sound
    sound = pygame.mixer.Sound(f"{DATA_PATH}audio/search_for_item.wav")
    # Play the sound
    sound.play()

def play_item_not_found():
    # Initialize pygame mixer
    pygame.mixer.init()
    # Load the sound
    sound = pygame.mixer.Sound(f"{DATA_PATH}audio/item_not_found.wav")
    # Play the sound
    sound.play()

def play_item_found():
    # Initialize pygame mixer
    pygame.mixer.init()
    # Load the sound
    sound = pygame.mixer.Sound(f"{DATA_PATH}audio/item_found.wav")
    # Play the sound
    sound.play()