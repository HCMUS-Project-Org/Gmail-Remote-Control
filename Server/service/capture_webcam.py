import cv2
#import os
#from . import shared_function as sf


def capture_webcam_image(default_value=None):
    # initialize the camera
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # check if camera is opened successfully
    if not camera.isOpened():
        return "Unable to open camera"
    else:
        # capture a frame from the camera
        bool, image = camera.read()

        if bool: 
            return image
        else:
            return "Unable to capture"

        # # specify the file path and name
        # file_path = os.path.join(sf.ASSET_PATH, "webcam_image.png")

        # # Save image
        # cv2.imwrite(file_path, image)

        # # release the camera
        # camera.release()
