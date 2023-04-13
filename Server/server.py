# Work with Image
from PIL import ImageGrab
import io


def capture_screen(self, client):
    INFO_SZ = 100

    img = ImageGrab.grab()
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')

    data = img_bytes.getvalue()

    # send frame size
    client.sendall(bytes(str(len(data)), "utf8"))

    # send frame data
    client.sendall(data)
