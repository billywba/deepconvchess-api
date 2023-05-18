import numpy as np

from sklearn.preprocessing import LabelEncoder

import tensorflow as tf
from tensorflow.keras.models import load_model


class ChessBoardPositionRecogniser:
    def __init__(self):
        self.model = load_model("./models/ResNet152_1684339957.h5")

        
        PIECE_LABELS = ['_', 'p', 'n', 'b', 'r', 'q', 'k', 'P', 'N', 'B', 'R', 'Q', 'K']
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(PIECE_LABELS)

    def retrieve_fen_from_image(self, image):
        X = self._retrieve_X_array(image)
        y_pred = self.model.predict(X)

        print(self.label_encoder.inverse_transform(np.argmax(y_pred, axis=1)))

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
    