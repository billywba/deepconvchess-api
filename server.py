from flask import Flask, request, jsonify

import base64
import io
import numpy as np

from PIL import Image, ImageOps

from tensorflow import convert_to_tensor

app = Flask(__name__)

@app.route('/')
def hello():
    return 'DEEPCONVCHESS'

@app.route('/image/process', methods=['POST'])
def process_image():
    base64_image = request.json.get('image')
    image_data = base64.b64decode(base64_image)

    image = Image.open(io.BytesIO(image_data))
    image = ImageOps.exif_transpose(image)
    image.save("test.jpg")

    image_array = np.array(image)
    tensor = convert_to_tensor(image_array)

    print(tensor)

    return jsonify({'message': 'image processed'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)