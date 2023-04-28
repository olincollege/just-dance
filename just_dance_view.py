import cv2


class JustDanceView:
    def __init__(self, model):
        self.model = model

    @staticmethod
    def display_frame(frame, window_name):
        cv2.imshow(window_name, frame)
        cv2.waitKey(10)
