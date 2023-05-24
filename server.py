from flask import Flask, request, jsonify

from core.ChessBoardPositionRecogniser import ChessBoardPositionRecogniser
from database.MoveStatisticsDatabase import MoveStatisticsDatabase

from utils.utils import convert_base64_image_to_image, extract_chess_board_from_image


app = Flask(__name__)

chess_board_position_recogniser = ChessBoardPositionRecogniser()
move_stats_db = MoveStatisticsDatabase(host='localhost', port=3306, username='root', password='root', database='move_statistics')


@app.route('/')
def hello():
    return 'DEEPCONVCHESS'

@app.route('/image/process', methods=['POST'])
def process_image():
    base64_image = request.json.get('image')
    
    image = convert_base64_image_to_image(base64_image)
    board_image = extract_chess_board_from_image(image)

    predicted_fen = chess_board_position_recogniser.retrieve_fen_from_image(board_image)
    print("Predicted FEN: %s" % predicted_fen)

    move_statistics = move_stats_db.get_statistics(predicted_fen)

    return jsonify(move_statistics)

@app.route('/stats', methods=['GET'])
def get_statistics():
    data = request.get_json()
    fen = data.get('fen')

    move_statistics = move_stats_db.get_statistics(fen)
    print(move_statistics)

    return jsonify(move_statistics)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)