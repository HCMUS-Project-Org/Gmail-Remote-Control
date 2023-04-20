import cv2
import os
from shared_function import *


def capture_webcam_image():
    # initialize the camera
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # check if camera is opened successfully
    if not camera.isOpened():
        print("Unable to open camera")
    else:
        # capture a frame from the camera
        _, image = camera.read()

        # specify the file path and name
        file_path = os.path.join(ASSET_PATH, "webcam_image.png")

        # Save image
        cv2.imwrite(file_path, image)

        # release the camera
        camera.release()


if __name__ == '__main__':
    capture_webcam_image()
