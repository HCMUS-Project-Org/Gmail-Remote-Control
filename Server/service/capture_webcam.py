import cv2
import os

IMG_PATH = "assets"


def capture_webcam_image():
    # initialize the camera
    camera = cv2.VideoCapture(0)

    # capture a frame from the camera
    ret, image = camera.read()

    # specify the file path and name
    file_path = os.path.join(IMG_PATH, "webcam_image.png")

    # Save image
    cv2.imwrite(file_path, image)

    # release the camera
    camera.release()

# TODO: check in window
