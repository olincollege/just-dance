"""
Set 'JustDanceController' class for the application
"""
import time
import numpy as np
import cv2
from playsound import playsound
from just_dance_view import JustDanceView


class JustDanceController:
    """A class that controls the execution of the Just Dance game.

    Attributes:
        model (object): A JustDanceModel object used to run inference on frames

        view (object): A JustDanceView object used to visualize the game

        angle_video (dict): A dictionary containing the angles of the body
            parts detected in the video frames

        angle_camera (dict): A dictionary containing the angles of the body
            parts detected in the camera frames

        timeout (float): The time at which the game will time out and exit

        cap1 (object): A VideoCapture object for the video file

        cap2 (object): A VideoCapture object for the camera

    Methods:
        __init__: Initialize a new `JustDanceController` object

        process_frame: Process a single frame of the video or camera capture

        process_frames: Process the frames from the video and camera capture

        release_capture: Release the video and camera captures

        close_windows: Close all open windows

        play_sound: Play a sound file
    """

    def __init__(self, model, video_path, camera_index=0):
        """
        Initialize a new `JustDanceController` object

        Args:
            model: A `JustDanceModel` object used for pose estimation

            video_path: A string representing the path to the video file

            camera_index: An integer representing the index of the camera
        """
        self.model = model
        self.view = JustDanceView(model=self.model)
        self.angle_video = {
            "left_arm": [],
            "right_arm": [],
            "left_elbow": [],
            "right_elbow": [],
            "left_thigh": [],
            "right_thigh": [],
            "left_leg": [],
            "right_leg": [],
        }
        self.angle_camera = {
            "left_arm": [],
            "right_arm": [],
            "left_elbow": [],
            "right_elbow": [],
            "left_thigh": [],
            "right_thigh": [],
            "left_leg": [],
            "right_leg": [],
        }
        self.timeout = time.time() + 300
        self.cap1 = cv2.VideoCapture(video_path)
        self.cap2 = cv2.VideoCapture(camera_index)

    def process_frame(self, frame):
        """
        Process a single frame of the video or camera capture

        Args:
            frame: A `numpy.ndarray` object representing the image frame

        Returns:
            key_points_with_scores: A `numpy.ndarray` object
                representing the keypoints with scores
        """
        img = cv2.resize(frame, (192, 192))
        img = np.expand_dims(img, axis=0)
        key_points_with_scores = self.model.run_inference(img)
        return key_points_with_scores

    def process_frames(self):
        """
        Process the frames from the video and camera capture
        """
        while self.cap1.isOpened():
            _, frame1 = self.cap1.read()
            _, frame2 = self.cap2.read()
            frame2 = cv2.flip(frame2, 1)

            key_points_with_scores_video = self.process_frame(frame1)
            key_points_with_scores_camera = self.process_frame(frame2)

            self.model.store_angles(
                self.angle_video, frame2, key_points_with_scores_video
            )
            self.model.store_angles(
                self.angle_camera, frame2, key_points_with_scores_camera
            )

            # Get the dimensions of frame1 and frame2
            height1, _, _ = frame1.shape
            height2, width2, _ = frame2.shape

            # Resize frame2 to have the same height as frame1
            if height1 != height2:
                scale_factor = height1 / height2
                width2 = int(width2 * scale_factor)
                height2 = height1
                frame2 = cv2.resize(frame2, (width2, height2))

            # Combine the video and camera frames horizontally
            combined_frame = np.concatenate((frame1, frame2), axis=1)

            # Resize the combined frame to fit the window size
            combined_frame = cv2.resize(
                combined_frame, (3840, 1600), interpolation=cv2.INTER_LINEAR
            )

            # Display the combined frame in a named window
            cv2.namedWindow("Just Dance", cv2.WINDOW_NORMAL)
            cv2.imshow("Just Dance", combined_frame)

            if cv2.waitKey(10) & 0xFF == 27:
                # Exit loop if 'q' key is pressed
                break

            if time.time() > self.timeout:
                print("Timeout reached! Exiting...")
                break

    def release_capture(self):
        """
        Release the video and camera captures
        """
        self.cap1.release()
        self.cap2.release()

    @staticmethod
    def close_windows():
        """
        Close all open windows
        """
        cv2.destroyAllWindows()

    @staticmethod
    def play_sound(song):
        """
        Play a sound file

        Args:
            song: A string representing the path to the sound file
        """
        playsound(song, False)
