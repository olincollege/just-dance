import tkinter as tk
from tkinter import ttk
from tkinter import font as tk_font
from just_dance_main import run_game

"""
colour palette: #2D1E29
#272D2B
#3D5E5E
#B3A478
#E6DCA6
"""

plays = 0


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tk_font.Font(
            family="Helvetica", size=18, weight="bold"
        )

        # the container is where we'll stack a bunch of frames
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
        x = (screen_width / 2) - (600 / 2)
        y = (screen_height / 2) - (300 / 2)

        # Set the position of the window to the center of the screen
        self.geometry(f"600x300+{int(x)}+{int(y)}")

        self.frames = {}

        for F in (StartPage, EndPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        if plays == 0:
            self.show_frame("StartPage", plays)
        else:
            self.show_frame("EndPage", plays)

    def show_frame(self, page_name, num_plays):
        """
        Show a frame for the given page name
        """
        num_plays += 1
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # song options
        self.songs = {
            "Shape of You": "shapeofyou",
            "Call Me Maybe": "callmemaybe",
            "Uptown Funk": "uptownfunk",
            "Muqabla (Hindi)": "muqabla",
            "Don't Start Now": "dontstartnow"
        }
        self.selected_song_key = next(iter(self.songs))
        self.selected_song = self.songs[self.selected_song_key]
        self.controller = controller
        self.plays = 0

        label = tk.Label(self, text="Choose a song below!",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=20)

        controller.title("Just Dance - Start Game")

        def dropdown_callback(*args):
            self.selected_song_key = self.dropdown_var.get()
            self.selected_song = self.songs[self.selected_song_key]

        # create the dropdown widget
        self.dropdown_var = tk.StringVar(self)
        self.dropdown_var.set(self.songs[self.selected_song_key])
        self.dropdown_var.trace("w", dropdown_callback)
        self.dropdown_menu = ttk.OptionMenu(self, self.dropdown_var,
                                            *self.songs)
        self.dropdown_menu.pack()

        start_button = tk.Button(
            self,
            text="Start Game",
            command=lambda:
            run_game(song=self.selected_song),
        )
        start_button.pack()

        end_button = tk.Button(
            self,
            text="Quit Game",
            command=lambda: quit(),
        )
        end_button.pack()


class EndPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(
            self, text="You have got great dancing moves!!!"
                       "You scored {score} points!",
            font=controller.title_font
        )
        label.pack(side="top", fill="x", pady=20)

        start_button = tk.Button(
            self,
            text="Play again!",
            command=lambda: controller.show_frame("StartPage"),
        )
        start_button.pack()

        end_button = tk.Button(
            self,
            text="Quit Game",
            command=lambda: quit(),
        )
        end_button.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
