import cv2
import os
from shared_function import *

ASSET_PATH = "../assets"
ASSET_PATH = convert_to_path(ASSET_PATH)


def capture_webcam_image():
    # initialize the camera
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # check if camera is opened successfully
    if not camera.isOpened():
        print("Unable to open camera")
    else:
        # capture a frame from the camera
        _, image = camera.read()

        # check directory and create if not exist
        if not check_file_exist(ASSET_PATH):
            os.mkdir(ASSET_PATH)

        # specify the file path and name
        file_path = os.path.join(ASSET_PATH, "webcam_image.png")
        print("file_path: ", file_path)

        # Save image
        cv2.imwrite(file_path, image)

        # release the camera
        camera.release()


if __name__ == "__main__":
    capture_webcam_image()
