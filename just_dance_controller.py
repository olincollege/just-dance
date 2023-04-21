import cv2
import numpy as np


class JustDanceController:
    def __init__(self, model):
        self.model = model

    def process_frame(self, frame):
        img = cv2.resize(frame, (192, 192))
        img = np.expand_dims(img, axis=0)
        key_points_with_scores = self.model.run_inference(img)
        return key_points_with_scores

    def choose_song_frame(self):
        # Method to choose the song
        pass

    def start_game(self):
        # Method to start the game
        pass

    def end_game(self):
        # Method to end the game
        pass

    @staticmethod
    def close_windows():
        cv2.destroyAllWindows()
