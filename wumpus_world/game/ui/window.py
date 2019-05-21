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

        self._width = 0
        self._height = 0

        self.title(Window.window_title)
        self.configure(background=Window.background_color)
        self._maximize()

        self._map = map
        self._board = Board(map, self)

        self._set_key_bindings()

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    def show(self):
        """Shows the window."""

        self._board.render()
        self.mainloop()

    def close(self, event=None):
        """Closes the window."""

        self.destroy()

    def render(self):
        self._board.render()

    def _maximize(self):
        """Sets the window size equal to the screen size."""

        self._width = self.winfo_screenwidth()
        self._height = self.winfo_screenheight()

        self.geometry("{}x{}".format(self.width, self.height))

    def _set_key_bindings(self):
        """Binds all required key bindings."""

        # Window close.
        self.bind("q", self.close)
        self.bind("<Escape>", self.close)

        # TODO: resize the board when the window is resized (<Configure> bind).
