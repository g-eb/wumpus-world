from tkinter import Tk
from .board import Board


class Window(Tk):
    """A class representing the main window of an application."""

    default_width = 1280
    default_height = 720
    min_width = 640
    min_height = 360
    window_title = "Wumpus World"
    background_color = "#21252b"

    def __init__(self, map):
        """Creates a new main window."""

        super().__init__()

        self.width = 0
        self.height = 0

        self.title(Window.window_title)
        self.configure(background=Window.background_color)
        self.__maximize()

        self.map = map
        self.board = Board(map, self)

        self.__set_key_bindings()

    def show(self):
        """Shows the window."""

        self.board.render()
        self.mainloop()

    def close(self, event):
        """Closes the window."""

        self.destroy()

    def __maximize(self):
        """Sets the window size equal to the screen size."""

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()

        self.geometry("{}x{}".format(self.width, self.height))

    def __set_key_bindings(self):
        """Binds all required key bindings."""

        # Window close.
        self.bind("q", self.close)
        self.bind("<Escape>", self.close)

        # Player movement.
        self.bind("w", self.__move_player)
        self.bind("a", self.__move_player)
        self.bind("s", self.__move_player)
        self.bind("d", self.__move_player)
        self.bind("<Up>", self.__move_player)
        self.bind("<Left>", self.__move_player)
        self.bind("<Down>", self.__move_player)
        self.bind("<Right>", self.__move_player)

        # TODO: resize the board when the window is resized (<Configure> bind).

    def __move_player(self, event):
        """Moves player when WASD or arrow keys were pressed."""

        # Transform arrow keys into WASD keys.
        keysym = {
            "Up": "w",
            "Left": "a",
            "Down": "s",
            "Right": "d"
        }.get(event.keysym, event.keysym)

        self.map.move(keysym)
        self.board.render()

    def __game_over(self, won):
        # TODO: a method showing info that game is over and the result (v/l).
        pass
