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
        """
        Calculate the angle between three joints using trigonometry.

        Args:
            frame: A dictionary of data from a single frame of a video feed
            key_points: A dictionary of coordinates of the user's
                joint key points
            start_index: An integer representing the index of the user's
                start joint
            middle_index: An integer representing the index of the user's
                middle joint
            end_index: An integer representing the index of the user's
                end joint
        
        Return
            A float representing the angle between three joints.
        """
        y_coordinate, x_coordinate, _ = frame.shape
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
    def store_angles(all_joint_angles, frame, key_points):
        """
        Store all angles between triplets of joints.
        
        Args:
            all_joint_angles: A dictionary representing all the calculated
                angles between a set of joints
            frame: A dictionary of data representing a single frame
                of a video feed
            key_points: A dictionary of coordinates of the user's
                joint key points
    
        """
        all_joint_angles["left_arm"].append(
            JustDanceModel.calculate_angle(frame, key_points, 5, 7, 9))
        all_joint_angles["right_arm"].append(
            JustDanceModel.calculate_angle(frame, key_points, 6, 8, 10))
        all_joint_angles["left_elbow"].append(
            JustDanceModel.calculate_angle(frame, key_points, 7, 5, 11))
        all_joint_angles["right_elbow"].append(
            JustDanceModel.calculate_angle(frame, key_points, 8, 6, 12))
        all_joint_angles["left_thigh"].append(
            JustDanceModel.calculate_angle(frame, key_points, 12, 11, 13))
        all_joint_angles["right_thigh"].append(
            JustDanceModel.calculate_angle(frame, key_points, 11, 12, 14))
        all_joint_angles["left_leg"].append(
            JustDanceModel.calculate_angle(frame, key_points, 11, 13, 15))
        all_joint_angles["right_leg"].append(
            JustDanceModel.calculate_angle(frame, key_points, 12, 14, 16))

    @staticmethod
    def score_calculator(angle_video, angle_camera, threshold):
        """
        Return a score based on how accurate the user's moves are
        compared to the video

        Args:
            angle_video: A list of angles for a joint in the input video.
            angle_camera: A list of angles for a joint in the user camera video.
            threshold: An integer representing the threshold angle difference
        
        Return:
            An integer representing the user's score based on the accuracy
            between the user's move and the video
        """
        accuracy_count = []
        video_array = np.array(angle_video)
        camera_array = np.array(angle_camera)

        angle_difference = (abs(video_array - camera_array)).tolist()

        for difference in angle_difference:
            if difference < threshold:
                accuracy_count.append(1)

        score = int((sum(accuracy_count)/len(angle_difference))*100)

        return score

    @staticmethod
    def final_score(all_angles_video, all_angles_camera, threshold):
        """
        Return a final score based on all the calculated scores for angles

        Args:
            all_angles_video: A dictionary representing all the calculated
                angles between a set of joints from a dance video
            all_angles_camera: A dictionary representing all the calculated
                angles between a set of joints from the user's camera feed
            threshold: An integer representing the score determining up to 
                how much counts as being the "correct move" for a
                valid score point


        """
        all_scores = []

        joints = ["left_arm", "right_arm", "left_elbow", "right_elbow",
                  "left_thigh", "right_thigh", "left_leg", "right_leg"]

        for joint in joints:
            all_scores.append(
                JustDanceModel.score_calculator(
                    all_angles_video[joint],
                    all_angles_camera[joint],
                    threshold))

        final_score = np.mean(all_scores)

        return final_score
