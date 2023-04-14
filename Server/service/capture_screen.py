from PIL import ImageGrab
import os

IMG_PATH = "assets"


def capture_screen():
    # capture the screen
    screenshot = ImageGrab.grab()

    # specify the file path and name
    file_path = os.path.join(IMG_PATH, "screenshot.png")

    # save the captured image
    screenshot.save(file_path)
