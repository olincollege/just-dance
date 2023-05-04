"""
Module to test functions for the Just Dance Game
"""
import csv
import pytest
from just_dance_score import get_current_score, get_leaderboard_scores
from just_dance_model import JustDanceModel
from just_dance_controller import JustDanceController


@pytest.fixture
def leaderboard_data():
    """
    The function  is a fixture that returns a list of scores
    for testing the leaderboard functionality of the Just Dance game.
    The list consists of 8 sub-lists, each containing a single string that
    represents a score value between 0 and 100. This fixture is used in the
    test_get_current_score() and test_get_leaderboard_scores() test functions
    to write test data to a temporary CSV file and to retrieve the top scores
    from the file, respectively.
    """
    return [
        ["90"],
        ["80"],
        ["70"],
        ["60"],
        ["50"],
        ["76"],
        ["93"],
        ["54"],
    ]


def test_get_current_score(leaderboard_data):
    # pylint: disable=redefined-outer-name
    """
    This function tests the get_current_score function which retrieves the
    current score from a CSV file. It first writes test data to a
    temporary test CSV file, then calls the get_current_score function and
    asserts that the score is within the valid range of 0 to 100.

    Args:
        leaderboard_data: test leaderboard csv file containing scores.
    """
    with open(
        "test/test.csv", "w"
    ) as file:  # pylint: disable=unspecified-encoding, line-too-long
        writer = csv.writer(file)
        writer.writerows(leaderboard_data)

    score = get_current_score("test/test.csv")
    assert 0 <= score <= 100


def test_get_leaderboard_scores(leaderboard_data):
    # pylint: disable=redefined-outer-name
    """
    This function tests the get_leaderboard_scores function which
    retrieves the top 5 scores from a CSV file. It first writes test data
    to a temporary test CSV file, then calls the get_leaderboard_scores
    function and asserts that the length of the returned top scores list is 5.
    Additionally, the function checks that the scores in the top_scores list
    are sorted in descending order.

    Args:
        leaderboard_data: test leaderboard csv file containing scores.
    """
    with open(
        "test/test.csv", "w"
    ) as file:  # pylint: disable=unspecified-encoding, line-too-long
        writer = csv.writer(file)
        writer.writerows(leaderboard_data)

    top_scores = get_leaderboard_scores("test/test.csv")
    assert len(top_scores) == 5

    # Check that scores are sorted in descending order
    for i in range(len(top_scores) - 1):
        assert top_scores[i] >= top_scores[i + 1]


def test_angles_in_range():
    """
    This function tests the angles in the Just Dance game and ensures that
    they are within the range of 0 to 180. It creates a new JustDanceModel
    and JustDanceController object using the test video file and model.
    Then it calls the process_frames function on the controller object to
    calculate the angles of the dance moves in the video. Finally,
    it iterates through all the angles in the angles_video and angles_camera
    dictionaries, and asserts that each angle is within the valid range.
    """
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
