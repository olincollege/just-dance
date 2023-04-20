import tensorflow as tf
import numpy as np


class JustDanceModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()

    def run_inference(self, input_image):
        input_image = tf.cast(input_image, dtype=tf.float32)

        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        self.interpreter.set_tensor(
            input_details[0]["index"], input_image.numpy())
        self.interpreter.invoke()

        key_points_with_scores = self.interpreter.get_tensor(
            output_details[0]["index"])

        return key_points_with_scores

    @staticmethod
    def calculate_angle(
            frame, key_points, start_index, middle_index, end_index):
        y_coordinate, x_coordinate, channel = frame.shape
        shaped = np.squeeze(np.multiply(
            key_points, [y_coordinate, x_coordinate, 1])
        )

        joint_start = np.array(
            [int(shaped[start_index][0]), int(shaped[start_index][1])]
        )
        joint_middle = np.array(
            [int(shaped[middle_index][0]), int(shaped[middle_index][1])]
        )
        joint_end = np.array(
            [int(shaped[end_index][0]), int(shaped[end_index][1])]
        )

        radians = np.arctan2(
            joint_end[1] - joint_middle[1], joint_end[0] - joint_middle[0]
        ) - np.arctan2(
            joint_start[1] - joint_middle[1], joint_start[0] - joint_middle[0]
        )
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle
