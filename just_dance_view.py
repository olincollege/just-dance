import cv2


class JustDanceView:
    """
       A class to display frames using OpenCV.

       Attributes:
           model (object): An object representing the model.
    """
    def __init__(self, model):
        """
        Initializes a new instance of the JustDanceView class.

        Args:
            model (object): An object representing
            the model used in the application.
        """
        self.model = model

    @staticmethod
    def display_frame(frame, window_name):
        """
        Displays a frame in a window using OpenCV.

        Args:
            frame (ndarray): The frame to be displayed.
            window_name (str): The name of the window to display the frame in.

        Returns:
            None
        """
        cv2.imshow(window_name, frame)
        cv2.waitKey(10)
