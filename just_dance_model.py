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

    @staticmethod
    def score_calculator(video, camera, threshold):
        """
        Return a score based on how accurate the user's moves are
        compared to the video

        Args:
            video: A list of angles between two specific joints.
            camera: A list of angles between two specific joints.
            threshold: An integer representing the threshold angle difference
        
        Return:video
            An integer representing the user's score based on the accuracy
            between the user's move and the video
        """
        accuracy_count = []
        video_array = np.array(video)
        camera_array = np.array(camera)
        angle_difference = (abs(video_array - camera_array )).tolist()
        for difference in angle_difference:
            if difference < threshold:
                accuracy_count.append(1)
        score = int((sum(accuracy_count)/len(angle_difference))*100)

        return score
