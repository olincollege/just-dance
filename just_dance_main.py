import cv2
import time
from just_dance_model import JustDanceModel
from just_dance_view import JustDanceView
from just_dance_controller import JustDanceController
from KEYPOINT import KEYPOINT_DICT, KEYPOINT_EDGE_INDS_TO_COLOR


class JustDanceApp:
    def __init__(self, model_path, video_path, camera_index):
        self.model = JustDanceModel(model_path=model_path)
        self.view = JustDanceView()
        self.controller = JustDanceController(model=self.model)
        self.cap1 = cv2.VideoCapture(video_path)
        self.cap2 = cv2.VideoCapture(camera_index)
        self.angle_video = []
        self.angle_camera = []
        self.timeout = time.time() + 300

    def process_frames(self):
        while self.cap1.isOpened():
            ret1, frame1 = self.cap1.read()
            ret2, frame2 = self.cap2.read()

            key_points_with_scores_video = self.controller.process_frame(frame1)
            key_points_with_scores_camera = self.controller.process_frame(frame2)

            self.view.draw_connections(
                frame1, key_points_with_scores_video,
                KEYPOINT_EDGE_INDS_TO_COLOR, 0.1
            )
            self.view.draw_key_points(frame1, key_points_with_scores_video, 0.1)
            self.angle_video.append(
                self.controller.calculate_angle(
                    frame1, key_points_with_scores_video, 6, 8, 10
                )
            )

            self.view.draw_connections(
                frame2, key_points_with_scores_camera,
                KEYPOINT_EDGE_INDS_TO_COLOR, 0.1
            )
            self.view.draw_key_points(
                frame2, key_points_with_scores_camera, 0.1
            )
            self.angle_camera.append(
                self.controller.calculate_angle(
                    frame2, key_points_with_scores_camera, 6, 8, 10
                )
            )

            self.view.display_frame(frame1, "Just Dance")
            self.view.display_frame(frame2, "You Dance")

            if cv2.waitKey(10) & 0xFF == 27:
                # Exit loop if 'q' key is pressed
                break

            if time.time() > self.timeout:
                print("Timeout reached. Exiting...")
                break

    def release_capture(self):
        self.cap1.release()
        self.cap2.release()

    def close_windows(self):
        self.view.close_windows()

    def print_angle_data(self):
        print("Angle data from Video:", self.angle_video)
        print("Angle data from Camera:", self.angle_camera)

    def run(self):
        self.process_frames()
        self.release_capture()
        self.close_windows()
        self.print_angle_data()
        # Perform game logic and display results
        # ... implementation ...


if __name__ == "__main__":
    # Instantiate JustDanceApp with model path, video path, and camera index
    app = JustDanceApp(
        model_path="model.tflite", video_path="test.mp4", camera_index=0
    )
    app.run()
