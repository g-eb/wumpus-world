import tkinter as tk
from .board import Board


class Window():
    default_width = 1280
    default_height = 720

    def __init__(self, map):
        width, height = self.__calc_window_size(map.width, map.height)
        self.map = map
        self.root = tk.Tk()
        self.board = Board(width, height, map, self.root)

        self.root.wm_title("Wumpus World")
        self.root.geometry("{}x{}".format(width, height))
        self.__set_key_bindings()

    def show(self):
        self.board.render()
        self.root.mainloop()

    def close(self, event):
        self.root.destroy()

    def __calc_window_size(self, map_width, map_height):
        map_width_in_pixels = map_width * Board.square_size
        map_height_in_pixels = map_height * Board.square_size
        map_width_fits = map_width_in_pixels <= Window.default_width
        map_height_fits = map_height_in_pixels <= Window.default_height

        if map_width_fits and map_height_fits:
            return (map_width_in_pixels, map_height_in_pixels)

        if map_width_fits:
            return (map_width_in_pixels, Window.default_height)

        if map_height_fits:
            return (Window.default_width, map_height_in_pixels)

        return (Window.default_width, Window.default_height)

    def __set_key_bindings(self):
        # Window close.
        self.root.bind("q", self.close)
        self.root.bind("<Escape>", self.close)

        # Player movement.
        self.root.bind("w", self.__move_player)
        self.root.bind("a", self.__move_player)
        self.root.bind("s", self.__move_player)
        self.root.bind("d", self.__move_player)
        self.root.bind("<Up>", self.__move_player)
        self.root.bind("<Left>", self.__move_player)
        self.root.bind("<Down>", self.__move_player)
        self.root.bind("<Right>", self.__move_player)

    def __move_player(self, event):
        keysym = {
            "Up": "w",
            "Left": "a",
            "Down": "s",
            "Right": "d"
        }.get(event.keysym, event.keysym)

        self.map.move(keysym)
        self.board.render()
