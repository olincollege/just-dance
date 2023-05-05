"""
Run a GUI for the user to input and call the application
"""
import sys
import time
import tkinter as tk
from tkinter import ttk
from tkinter import font as tk_font
from mutagen.mp3 import MP3
from just_dance_main import run_game
from just_dance_gui_score import Score

# colour palette:
# #2D1E29
# #272D2B
# #3D5E5E
# #B3A478
# #E6DCA6


class App(tk.Tk):
    """
    The main application window that inherits from `tk.Tk`

    Attributes:
        title_font (tk_font.Font): The font used for the title label
        frames (dict): A dictionary of the frames used in the application

    Methods:
        __init__: Initialize the application window
        show_frame: Show the specified frame
        start_timer: Starts a timer when the program is run
        update_timer: Updates the program timer
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

        for F in (StartPage, EndPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # Put all the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        start_page = StartPage(parent=container, controller=self)
        self.song_length = start_page.get_song_length()
        self.start_timer()

    def show_frame(self, page_name):
        """
        Show a frame for the given page name

        Args:
            page_name (str): The name of the page to show
        """
        frame = self.frames[page_name]
        frame.tkraise()

    def start_timer(self):
        """
        Starts a timer and stores the start time.
        The timer will be updated by calling the `update_timer` method.
        """
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        """
        Updates the timer by calculating the elapsed time since the timer
        was started.

        If the elapsed time is less than the specified song length,
        this method will schedule itself to be called again after
        the song length has elapsed. Otherwise, it will switch to
        the "EndPage" frame by calling the `show_frame` method.
        """
        current_time = time.time() - self.start_time
        if current_time < self.song_length:
            self.after(self.song_length, self.update_timer)
        else:
            self.show_frame("EndPage")


class StartPage(tk.Frame):
    """
    The start page frame that inherits from `tk.Frame`

    Attributes:
        songs (dict): A dictionary of the available songs
        selected_song_key (str): The key for the currently selected song
        selected_song (str): The value for the currently selected song
        controller (App): The application window

    Methods:
        __init__: Initialize the StartPage class and set up the GUI elements
        get_song_length: Extracts the length of the selected audio.
    """

    def __init__(self, parent, controller):
        """
        Initialize the StartPage object and set up the GUI elements

        Args:
            parent (tk.Tk): The parent widget
            controller (App): The application window
        """
        tk.Frame.__init__(self, parent)
        # Song options
        self.songs = {
            "Cheap Thrills": "cheapthrills",
            "Call Me Maybe": "callmemaybe",
            "Uptown Funk": "uptownfunk",
            "Ghungroo (Hindi)": "ghungroo",
            "Don't Start Now": "dontstartnow",
        }
        self.selected_song_key = next(iter(self.songs))
        self.selected_song = self.songs[self.selected_song_key]
        self.controller = controller

        label = tk.Label(
            self, text="Choose a song below!", font=controller.title_font
        )
        label.pack(side="top", fill="x", pady=20)

        controller.title("Just Dance - Game")

        def dropdown_callback(*args):  # pylint: disable=unused-argument
            self.selected_song_key = self.dropdown_var.get()
            self.selected_song = self.songs[self.selected_song_key]

        # create the dropdown widget
        self.dropdown_var = tk.StringVar(self)
        self.dropdown_var.set(self.songs[self.selected_song_key])
        self.dropdown_var.trace("w", dropdown_callback)
        self.dropdown_menu = ttk.OptionMenu(
            self, self.dropdown_var, *self.songs
        )
        self.dropdown_menu.pack()

        start_button = tk.Button(
            self,
            text="Start Game",
            command=lambda: run_game(song=self.selected_song),
        )
        start_button.pack()

        end_button = tk.Button(
            self,
            text="Quit Game",
            command=lambda: sys.exit(),  # pylint: disable=unnecessary-lambda
        )
        end_button.pack()

    def get_song_length(self):
        """
        Gets the length of the selected song in seconds.

        Returns:
            The length of the selected song in seconds as an integer.
        """
        song_audio = MP3("songs_audio/" + self.selected_song + ".mp3")
        return int(song_audio.info.length)


class EndPage(tk.Frame):
    """
    The end page frame that inherits from `tk.Frame`

    Attributes:
        controller (App): The application window

    Methods:
        __init__: Initialize the EndPage object and set up the GUI elements.
    """

    def __init__(self, parent, controller):
        """
        Initialize the EndPage object and set up the GUI elements.

        Args:
            parent (tk.Tk): The parent widget
            controller (App): The application window
        """
        tk.Frame.__init__(self, parent)
        self.controller = controller

        controller.title("Just Dance - Game")

        label = tk.Label(
            self,
            text="You have got great dancing moves!!!",
            font=controller.title_font,
        )
        label.pack(side="top", fill="x", pady=20)

        start_button = tk.Button(
            self,
            text="View your score!",
            command=lambda: Score(),  # pylint: disable=unnecessary-lambda
        )
        start_button.pack()

        end_button = tk.Button(
            self,
            text="Quit Game",
            command=lambda: sys.exit(),  # pylint: disable=unnecessary-lambda
        )
        end_button.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
