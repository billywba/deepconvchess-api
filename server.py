from flask import Flask, request, jsonify

from utils import convert_base64_image_to_image, extract_chess_board_from_image


app = Flask(__name__)

@app.route('/')
def hello():
    return 'DEEPCONVCHESS'

@app.route('/image/process', methods=['POST'])
def process_image():
    base64_image = request.json.get('image')
    
    image = convert_base64_image_to_image(base64_image)
    board_image = extract_chess_board_from_image(image)


    return jsonify({'message': 'image processed'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)