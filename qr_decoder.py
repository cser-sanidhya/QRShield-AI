from pyzbar.pyzbar import decode
from PIL import Image

def decode_qr(image_path):
    image = Image.open(image_path)

    decoded_objects = decode(image)

    if decoded_objects:
        return decoded_objects[0].data.decode("utf-8")

    return "No QR code found"