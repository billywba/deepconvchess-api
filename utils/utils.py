import base64

import io
import numpy as np

from PIL import Image, ImageOps
from tensorflow import convert_to_tensor


def convert_base64_image_to_image(image_base64):
    image_data = base64.b64decode(image_base64)

    image = Image.open(io.BytesIO(image_data))
    image = ImageOps.exif_transpose(image)

    return image


def extract_chess_board_from_image(image):
    IMG_WIDTH, IMG_HEIGHT = image.size

    start_x = 0 
    start_y = (IMG_HEIGHT - IMG_WIDTH) // 2

    # Crop to retrieve the middle square of the image
    extracted_image = image.crop((start_x, start_y, start_x + IMG_WIDTH, start_y + IMG_WIDTH))
    extracted_image = extracted_image.resize((1280, 1280))

    return extracted_image
