from PIL import ImageGrab
import os
#from . import shared_function as sf


def capture_screen(default_value=None):
    # capture the screen
    return ImageGrab.grab()
