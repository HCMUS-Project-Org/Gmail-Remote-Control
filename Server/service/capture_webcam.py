import cv2
from PIL import Image


def capture_webcam_image(default_value=None):
    # initialize the camera
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # check if camera is opened successfully
    if not camera.isOpened():
        return "<div class='mb-2'><b>Capture webcam:</b> " + "Unable to open camera" + "</div>"
    else:
        # capture a frame from the camera
        bool, image = camera.read()

        if bool:
            # convert color space from BGR to RGB
            rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # create a PIL Image from the numpy array
            pil_image = Image.fromarray(rgb_frame)

            return pil_image
        else:
            return "<div class='mb-2'><b>Capture webcam:</b> " + "Unable to capture" + "</div>"
