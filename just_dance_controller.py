import cv2
import numpy as np
from KEYPOINT import KEYPOINT_DICT, KEYPOINT_EDGE_INDICES_TO_COLOR
import time
from just_dance_view import JustDanceView


class JustDanceController:
    def __init__(self, model, video_path, camera_index):
        self.model = model
        self.view = JustDanceView(model=self.model)
        self.angle_video = []
        self.angle_camera = []
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

            key_points_with_scores_video = \
                self.process_frame(frame1)
            key_points_with_scores_camera = \
                self.process_frame(frame2)

            self.view.draw_connections(
                frame1, key_points_with_scores_video,
                KEYPOINT_EDGE_INDICES_TO_COLOR, 0.1
            )
            self.view.draw_key_points(frame1, key_points_with_scores_video, 0.1)
            self.angle_video.append(
                self.model.calculate_angle(
                    frame1, key_points_with_scores_video, 6, 8, 10
                )
            )

            self.view.draw_connections(
                frame2, key_points_with_scores_camera,
                KEYPOINT_EDGE_INDICES_TO_COLOR, 0.1
            )
            self.view.draw_key_points(
                frame2, key_points_with_scores_camera, 0.1
            )
            self.angle_camera.append(
                self.model.calculate_angle(
                    frame2, key_points_with_scores_camera, 6, 8, 10
                )
            )

            self.view.display_frame(frame1, "Just Dance")
            self.view.display_frame(frame2, "You Dance")

            if cv2.waitKey(10) & 0xFF == 27:
                # Exit loop if 'q' key is pressed
                break

            if time.time() > self.timeout:
                print("Timeout reached! Exiting...")
                break

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
