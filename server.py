from flask import Flask, request, jsonify

from core.ChessBoardPositionRecogniser import ChessBoardPositionRecogniser

from utils.utils import convert_base64_image_to_image, extract_chess_board_from_image


app = Flask(__name__)

chess_board_position_recogniser = ChessBoardPositionRecogniser()

@app.route('/')
def hello():
    return 'DEEPCONVCHESS'

@app.route('/image/process', methods=['POST'])
def process_image():
    base64_image = request.json.get('image')
    
    image = convert_base64_image_to_image(base64_image)
    board_image = extract_chess_board_from_image(image)

    predicted_fen = chess_board_position_recogniser.retrieve_fen_from_image(board_image)
    print(predicted_fen)

    return jsonify({'message': 'image processed'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)