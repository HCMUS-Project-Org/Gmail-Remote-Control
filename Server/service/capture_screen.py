from PIL import ImageGrab
import os
#from . import shared_function as sf


def capture_screen(default_value=None):
    # capture the screen
    return ImageGrab.grab()

    # # specify the file path and name
    # file_path = os.path.join(sf.ASSET_PATH, "screenshot.png")

    # # save the captured image
    # screenshot.save(file_path)
