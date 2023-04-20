from PIL import ImageGrab
import os
from shared_function import *


def capture_screen():
    # capture the screen
    screenshot = ImageGrab.grab()

    # specify the file path and name
    file_path = os.path.join(ASSET_PATH, "screenshot.png")

    # save the captured image
    screenshot.save(file_path)
