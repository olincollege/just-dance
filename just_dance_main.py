"""
Set 'JustDanceGame' class and 'run_game' function to link all classes together
"""
from just_dance_model import JustDanceModel
from just_dance_view import JustDanceView
from just_dance_controller import JustDanceController


class JustDanceGame:
    """
    A class to represent the application run using the JustDanceModel,
    JustDanceView, JustDanceController classes

    Attributes:
        model: An object representing the application model

        view: An object representing the application display

        controller: An object representing the application
            controller using the user input

    Methods:
        run: Run the JustDance Application
    """

    def __init__(self, model_path, video_path, camera_index):
        """
        Initialize a new instance of the JustDanceGame Class

        Args:
            model_path: An object representing the TensorFlow model path

            video_path: An object representing the dance video file path

            camera_index: An object representing the camera index for
                the user input camera feed
        """
        self.model = JustDanceModel(model_path=model_path)
        self.view = JustDanceView(model=self.model)
        self.controller = JustDanceController(
            model=self.model, video_path=video_path, camera_index=camera_index
        )

    def run(self, song):
        """
        Run the JustDance application

        Args:
            song: A string representing the chosen for the user to
            dance to
        """
        self.controller.play_sound("songs_audio/" + song + ".mp3")
        self.controller.process_frames()
        self.controller.release_capture()
        self.controller.close_windows()


def run_game(song):
    """
    Create an instance of the JustDanceGame class and
    run the game based on the chosen song

    Args:
        song: A string representing the chosen song for the user
            dance to
    """
    game = JustDanceGame(
        model_path="model/model.tflite",
        video_path="songs/" + song + ".mp4",
        camera_index=0,
    )
    game.run(song)
