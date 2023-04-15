# Work with Image
import service.capture_screen as cs
import service.capture_webcam as cw
import service.mac_address as mac
import service.app_process as ap

ASSET_PATH = "assets"

command = []

if __name__ == "__main__":
    # TODO: combine all check and create Assets folder in this file
    msg = "SCREEN"

    if "SCREEN" in msg:
        cs.capture_screen()
    elif "WEBCAM" in msg:
        cw.capture_webcam_image()
    elif "MAC" in msg:
        mac.mac_address()
    elif "APP_PRO" in msg:
        ap.app_process()

    # # capture the screen
    # server.capture_screen()

    # # get the mac address
    # mac_address = server.get_mac_address()
    # print(mac_address)

    # capture an image by the camera
    # server.capture_webcam_image()
