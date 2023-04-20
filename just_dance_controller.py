import numpy as np
import cv2


class JustDanceController:
    def __init__(self, model):
        self.model = model

    def calculate_angle(self, frame, key_points, start_index, middle_index, end_index):
        y_coordinate, x_coordinate, channel = frame.shape
        shaped = np.squeeze(np.multiply(key_points, [y_coordinate, x_coordinate, 1]))

        joint_start = np.array(
            [int(shaped[start_index][0]), int(shaped[start_index][1])]
        )
        joint_middle = np.array(
            [int(shaped[middle_index][0]), int(shaped[middle_index][1])]
        )
        joint_end = np.array([int(shaped[end_index][0]), int(shaped[end_index][1])])

        radians = np.arctan2(
            joint_end[1] - joint_middle[1], joint_end[0] - joint_middle[0]
        ) - np.arctan2(
            joint_start[1] - joint_middle[1], joint_start[0] - joint_middle[0]
        )
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    def process_frame(self, frame):
        img = cv2.resize(frame, (192, 192))
        img = np.expand_dims(img, axis=0)
        key_points_with_scores = self.model.run_inference(img)
        return key_points_with_scores
