import chess

import numpy as np

from sklearn.preprocessing import LabelEncoder

import tensorflow as tf
from tensorflow.keras.models import load_model


class ChessBoardPositionRecogniser:
    def __init__(self):
        self.model = load_model("./models/MobileNetV3Large_1684439918.h5")
        
        PIECE_LABELS = ['_', 'p', 'n', 'b', 'r', 'q', 'k', 'P', 'N', 'B', 'R', 'Q', 'K']
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(PIECE_LABELS)

    def retrieve_fen_from_image(self, image):
        X = self._retrieve_X_array(image)
        
        y_pred = self.model.predict(X)
        y_pred_labelled = self.label_encoder.inverse_transform(np.argmax(y_pred, axis=1))

        predicted_fen = self._convert_array_to_fen(y_pred_labelled)
        
        return predicted_fen

    def _retrieve_X_array(self, image):
        X = []
        IMG_WIDTH, IMG_HEIGHT = image.size

        # Crop each image into 64 sections, one for each tile on the board
        for i in range(8):
            for j in range(8):
                crop_x = j * IMG_WIDTH // 8
                crop_y = i * IMG_HEIGHT // 8
                img_crop = image.crop((crop_x, crop_y, crop_x + IMG_WIDTH // 8, crop_y + IMG_HEIGHT // 8))

                X.append(np.array(img_crop))

        X = np.array(X)

        return X
    
    def _convert_array_to_fen(self, piece_array):
        board = chess.Board("8/8/8/8/8/8/8/8")
        
        for i in range(0, len(piece_array)):
            if piece_array[i] != '_':
                piece = chess.Piece.from_symbol(piece_array[i])
                square = chess.SQUARES[(7 - (i // 8)) * 8 + (i % 8)]
                board.set_piece_at(square, piece)

        return board.fen().split(" ")[0]
