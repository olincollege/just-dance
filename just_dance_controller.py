import cv2
import numpy as np
import time
from playsound import playsound
from just_dance_view import JustDanceView


class JustDanceController:
    def __init__(self, model, video_path, camera_index=0):
        self.model = model
        self.view = JustDanceView(model=self.model)
        self.angle_video = {"left_arm": [], "right_arm": [],
                            "left_elbow": [], "right_elbow": [],
                            "left_thigh": [], "right_thigh": [],
                            "left_leg": [], "right_leg": []}
        self.angle_camera = {"left_arm": [], "right_arm": [],
                             "left_elbow": [], "right_elbow": [],
                             "left_thigh": [], "right_thigh": [],
                             "left_leg": [], "right_leg": []}
        self.timeout = time.time() + 300
        self.cap1 = cv2.VideoCapture(video_path)
        self.cap2 = cv2.VideoCapture(camera_index)

    def process_frame(self, frame):
        img = cv2.resize(frame, (192, 192))
        img = np.expand_dims(img, axis=0)
        key_points_with_scores = self.model.run_inference(img)
        return key_points_with_scores

    def process_frames(self):
        while self.cap1.isOpened():
            ret1, frame1 = self.cap1.read()
            ret2, frame2 = self.cap2.read()
            frame2 = cv2.flip(frame2, 1)

            key_points_with_scores_video = self.process_frame(frame1)
            key_points_with_scores_camera = self.process_frame(frame2)

            self.model.store_angles(
                self.angle_video, frame2, key_points_with_scores_video)
            self.model.store_angles(
                self.angle_camera, frame2, key_points_with_scores_camera)

            # Get the dimensions of frame1 and frame2
            height1, width1, _ = frame1.shape
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
        self.cap1.release()
        self.cap2.release()

    @staticmethod
    def close_windows():
        cv2.destroyAllWindows()

    @staticmethod
    def play_sound(song):
        playsound(song, False)
