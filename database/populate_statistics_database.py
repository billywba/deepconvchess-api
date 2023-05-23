from pathlib import Path

import chess
import chess.pgn
import io

from MoveStatisticsDatabase import MoveStatisticsDatabase


def process_pgn_game(pgn):
    game = chess.pgn.read_game(io.StringIO(pgn))

    board = game.board()
    GAME_WINNER = get_winner_from_game(game)

    for move in game.mainline_moves():
        fen = board.fen().split(" ")[0]

        move_stats_db.insert_statistic(fen, board.san(move), GAME_WINNER)
        
        board.push(move)
    

def get_winner_from_game(game):
    result = game.headers.get("Result")
    winner = ""

    if result == "1-0":
        winner = "white"
    elif result == "0-1":
        winner = "black"
    elif result == "1/2-1/2":
        winner = "draw"
    else:
        winner = "Unknown"

    return winner


if __name__ == "__main__":
    # Initialise database connection
    move_stats_db = MoveStatisticsDatabase(host='localhost', port=3306, username='root', password='root', database='move_statistics')

    # Open each .pgn file in /pgn and process the FENs
    for pgn_file_path in Path("./pgn").iterdir():
        print("Opening %s" % pgn_file_path)
        with open(pgn_file_path) as pgn_file:
            while True:
                game = chess.pgn.read_game(pgn_file)
                if game is None:
                    break

                pgn = str(game)
                process_pgn_game(pgn)
