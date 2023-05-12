import cv2
from PIL import Image
#import os
#from . import shared_function as sf


def capture_webcam_image(default_value=None):
    # initialize the camera
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # check if camera is opened successfully
    if not camera.isOpened():
        return "<p><b><u>++++CAPTURE WEBCAM++++</u></b></p>\n" + "Unable to open camera"
    else:
        # capture a frame from the camera
        bool, image = camera.read()

        if bool: 
            #convert color space from BGR to RGB
            rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # create a PIL Image from the numpy array
            pil_image = Image.fromarray(rgb_frame)

            return pil_image
        else:
            return "<p><b><u>++++CAPTURE WEBCAM++++</u></b></p>\n" + "Unable to capture"

        # # specify the file path and name
        # file_path = os.path.join(sf.ASSET_PATH, "webcam_image.png")

        # # Save image
        # cv2.imwrite(file_path, image)

        # # release the camera
        # camera.release()
