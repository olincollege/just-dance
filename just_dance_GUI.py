import tkinter as tk
from tkinter import ttk
from tkinter import font as tk_font
from just_dance_main import JustDanceGame, run_game

"""
colour palette: #2D1E29
#272D2B
#3D5E5E
#B3A478
#E6DCA6
"""


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
        self.geometry("500x200")

        self.frames = {}
        for F in (StartPage, PageOne, EndPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """
        Show a frame for the given page name
        """
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # song options
        self.songs = {
            "Shape of You": "shapeofyou.mp4",
            "Call Me Maybe": "callmemaybe.mp4",
            "Uptown Funk": "uptownfunk.mp4",
            "Muqabla (Hindi)": "muqabla.mp4",
            "Don't Start Now": "dontstartnow.mp4"
        }
        self.selected_song_key = next(iter(self.songs))
        self.selected_song = self.songs[self.selected_song_key]
        self.controller = controller

        label = tk.Label(self, text="Run Game", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        controller.title("Choose a song")

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
            command=lambda: run_game(song="songs/" + self.selected_song),
        )
        start_button.pack()

        end_button = tk.Button(
            self,
            text="End Game",
            command=lambda: controller.show_frame("EndPage"),
        )
        end_button.pack()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(
            self, text="This is page 1", font=controller.title_font
        )
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(
            self,
            text="Go to the start page",
            command=lambda: controller.show_frame("StartPage"),
        )
        button.pack()


class EndPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.game = JustDanceGame(
            model_path="model/model.tflite",
            video_path="songs/shapeofyou.mp4",
            camera_index=0
        )

        label = tk.Label(
            self, text="You have got great dancing moves!!!",
            font=controller.title_font
        )
        label.pack(side="top", fill="x", pady=10)
        start_button = tk.Button(
            self,
            text="Go back to the start page",
            command=lambda: controller.show_frame("StartPage"),
        )
        start_button.pack()
        end_button = tk.Button(
            self,
            text="Quit Game",
            command=lambda: self.game.end_game(),
        )
        end_button.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
