import pytest
import csv
from just_dance_score import give_current_score
from just_dance_model import JustDanceModel
from just_dance_controller import JustDanceController


@pytest.fixture
def leaderboard_data():
    return [
        ['90'],
        ['80'],
        ['70'],
        ['60'],
        ['50'],
    ]


def test_give_current_score(leaderboard_data):
    with open('test/test.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(leaderboard_data)

    score = give_current_score('test/test.csv')
    assert 0 <= score <= 100


def test_angles_in_range():
    model = JustDanceModel(model_path="model/model.tflite")
    controller = JustDanceController(model, "test/test.mp4", 0)
    controller.process_frames()
    controller.release_capture()

    # Iterate through all the angles
    for angle_list in controller.angles_video.values():
        for angle in angle_list:
            assert 0 <= angle <= 180

    for angle_list in controller.angles_camera.values():
        for angle in angle_list:
            assert 0 <= angle <= 180
