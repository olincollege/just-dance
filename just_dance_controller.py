"""
Set 'JustDanceController' class for the application
"""
import sys
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
        angles_video (dict): A dictionary containing the angles of the body
            parts detected in the video frames
        angles_camera (dict): A dictionary containing the angles of the body
            parts detected in the camera frames
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
        self.angles_video = {
            "left_arm": [],
            "right_arm": [],
            "left_elbow": [],
            "right_elbow": [],
            "left_thigh": [],
            "right_thigh": [],
            "left_leg": [],
            "right_leg": [],
        }
        self.angles_camera = {
            "left_arm": [],
            "right_arm": [],
            "left_elbow": [],
            "right_elbow": [],
            "left_thigh": [],
            "right_thigh": [],
            "left_leg": [],
            "right_leg": [],
        }
        self.cap1 = cv2.VideoCapture(video_path)  # pylint: disable=no-member
        self.cap2 = cv2.VideoCapture(camera_index)  # pylint: disable=no-member
        self.frame1_rate = self.cap1.get(
            cv2.CAP_PROP_FPS
        )  # pylint: disable=no-member

    def process_frame(self, frame):
        """
        Process a single frame of the video or camera capture

        Args:
            frame: A `numpy.ndarray` object representing the image frame

        Returns:
            key_points_with_scores: A `numpy.ndarray` object
                representing the key points with scores
        """
        img = cv2.resize(frame, (192, 192))  # pylint: disable=no-member
        img = np.expand_dims(img, axis=0)
        key_points_with_scores = self.model.run_inference(img)
        return key_points_with_scores

    def process_frames(self):
        """
        Process the frames from the video and camera capture
        """
        counter = 0

        while self.cap1.isOpened():
            start_time = time.time()
            _, frame1 = self.cap1.read()
            _, frame2 = self.cap2.read()
            frame2 = cv2.flip(frame2, 1)  # pylint: disable=no-member

            if counter == 0:
                key_points_with_scores_video = self.process_frame(frame1)
                key_points_with_scores_camera = self.process_frame(frame2)

                self.model.store_angles(
                    self.angles_video, frame2, key_points_with_scores_video
                )
                self.model.store_angles(
                    self.angles_camera, frame2, key_points_with_scores_camera
                )

            counter = (counter + 1) % 100

            if frame1 is not None and frame2 is not None:
                # Get the dimensions of frame1 and frame2
                height1, _, _ = frame1.shape
                height2, width2, _ = frame2.shape
            else:
                break

            # Resize frame2 to have the same height as frame1
            if height1 != height2:
                scale_factor = height1 / height2
                width2 = int(width2 * scale_factor)
                height2 = height1
                frame2 = cv2.resize(
                    frame2, (width2, height2)
                )  # pylint: disable=no-member

            # Combine the video and camera frames horizontally
            combined_frame = np.concatenate((frame1, frame2), axis=1)

            # Resize the combined frame to fit the window size
            combined_frame = cv2.resize(  # pylint: disable=no-member
                combined_frame,
                (3840, 1600),
                interpolation=cv2.INTER_LINEAR,  # pylint: disable=no-member
            )

            # Display the combined frame in a named window
            cv2.namedWindow(
                "Just Dance", cv2.WINDOW_NORMAL
            )  # pylint: disable=no-member
            cv2.imshow(
                "Just Dance", combined_frame
            )  # pylint: disable=no-member

            if cv2.waitKey(1) & 0xFF == ord("q"):  # pylint: disable=no-member
                # Exit program if 'q' key is pressed
                sys.exit()

            elapsed_time = time.time() - start_time
            frame_delay = max(
                1, int(1000 / self.frame1_rate) - int(elapsed_time * 1000)
            )
            time.sleep(frame_delay / 1000.0)

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
        cv2.destroyAllWindows()  # pylint: disable=no-member

    @staticmethod
    def play_sound(song):
        """
        Play a sound file

        Args:
            song: A string representing the path to the sound file
        """
        playsound(song, False)
