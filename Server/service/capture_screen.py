from PIL import ImageGrab
import os
from shared_function import *
from capture_webcam import IMG_PATH


def capture_screen():
    # capture the screen
    screenshot = ImageGrab.grab()

    # check directory and create if not exist
    if not check_file_exist(IMG_PATH):
        os.mkdir(IMG_PATH)

    # specify the file path and name
    file_path = os.path.join(IMG_PATH, "screenshot.png")

    # save the captured image
    screenshot.save(file_path)
