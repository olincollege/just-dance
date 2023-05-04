"""
Run a GUI for the user to display score and leaderboard
"""
import sys
import tkinter as tk
from tkinter import font as tk_font
from just_dance_score import give_current_score

# colour palette:
# #2D1E29
# #272D2B
# #3D5E5E
# #B3A478
# #E6DCA6


class Score(tk.Tk):
    """
    The score window that inherits from `tk.Tk`

    Attributes:
        title_font (tk_font.Font): The font used for the title label
        frames (dict): A dictionary of the frames used in the application

    Methods:
        __init__: Initialize the application window
        show_frame: Show the specified frame
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize the application window

        Args:
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        """
        tk.Tk.__init__(self, *args, **kwargs)

        self.start_time = None

        self.title_font = tk_font.Font(
            family="Helvetica", size=18, weight="bold"
        )

        # The container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the x and y coordinates for the Tkinter window
        x_coord = (screen_width / 2) - (600 / 2)
        y_coord = (screen_height / 2) - (300 / 2)

        # Set the position of the window to the center of the screen
        self.geometry(f"600x300+{int(x_coord)}+{int(y_coord)}")

        self.frames = {}

        for F in (ScorePage, LeaderboardPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # Put all the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("ScorePage")

    def show_frame(self, page_name):
        """
        Show a frame for the given page name

        Args:
            page_name (str): The name of the page to show
        """
        frame = self.frames[page_name]
        frame.tkraise()


class ScorePage(tk.Frame):
    def __init__(self, parent, controller):
        """
        Initialize the EndPage object and set up the GUI elements.

        Args:
            parent (tk.Tk): The parent widget
            controller (App): The application window
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        current_score = give_current_score("leaderboard.csv")

        label = tk.Label(
            self,
            text=(
                f"Your score is {current_score}.\n"
            ),
            font=controller.title_font
        )
        label.pack(side="top", fill="x", pady=20)

        leaderboard_button = tk.Button(
            self,
            text="View Leaderboard",
            command=lambda: controller.show_frame("LeaderboardPage")
        )
        leaderboard_button.pack()

        end_button = tk.Button(
            self,
            text="Quit Game",
            command=lambda: sys.exit()
        )
        end_button.pack()


class LeaderboardPage(tk.Frame):
    def __init__(self, parent, controller):
        """
        Initialize the EndPage object and set up the GUI elements.

        Args:
            parent (tk.Tk): The parent widget
            controller (App): The application window
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(
            self,
            text="Leaderboard",
            font=controller.title_font
        )
        label.pack(side="top", fill="x", pady=20)

        score_button = tk.Button(
            self,
            text="Go back to the Score Page",
            command=lambda: controller.show_frame("ScorePage")
        )
        score_button.pack()


if __name__ == "__main__":
    app = Score()
    app.mainloop()
