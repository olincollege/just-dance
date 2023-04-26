from just_dance_model import JustDanceModel
from just_dance_view import JustDanceView
from just_dance_controller import JustDanceController
from playsound import playsound


class JustDanceGame:
    def __init__(self, model_path, video_path, camera_index):
        self.model = JustDanceModel(model_path=model_path)
        self.view = JustDanceView(model=self.model)

        self.controller = JustDanceController(
            model=self.model, video_path=video_path, camera_index=camera_index
        )

    def run(self):
        playsound("test.mp3", False)
        self.controller.process_frames()
        self.controller.release_capture()
        self.controller.close_windows()


def run_game():
    game = JustDanceGame(
        model_path="model.tflite", video_path="test.mp4", camera_index=0
    )

    game.run()


# run_game()
