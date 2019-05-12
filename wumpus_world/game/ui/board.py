import tkinter as tk


def is_odd(x):
    return x % 2 == 1


def is_even(x):
    return x % 2 == 0


class Board(tk.Canvas):
    square_size = 64
    max_elements_per_square = 5
    element_radius = 8

    def __init__(self, window_width, window_height, map, master=None):
        super().__init__(master, width=window_width, height=window_height)

        self.width = map.width
        self.height = map.height
        self.squares = map.squares

        self.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                window_x = x * Board.square_size
                window_y = y * Board.square_size

                self.create_rectangle(
                    window_x,
                    window_y,
                    window_x + Board.square_size,
                    window_y + Board.square_size,
                    width=1,
                    outline="#3f3f3f",
                    fill="#e0e0e0"
                )

                self.__render_square_elements(x, y, self.squares[y][x])

    def __render_square_elements(self, x, y, square):
        center_x = int(Board.square_size * (x + 0.5))
        center_y = int(Board.square_size * (y + 0.5))
        elements = sorted(
            square.contains, key=lambda el: el.__class__.__name__
        )
        n = len(elements)

        if n == 1:
            self.create_oval(
                center_x - Board.element_radius,
                center_y - Board.element_radius,
                center_x + Board.element_radius,
                center_y + Board.element_radius,
                width=0,
                fill=elements[0].color
            )
        elif n == 2:
            self.create_oval(
                center_x - 3 * Board.element_radius,
                center_y - Board.element_radius,
                center_x - Board.element_radius,
                center_y + Board.element_radius,
                width=0,
                fill=elements[0].color
            )
            self.create_oval(
                center_x + Board.element_radius,
                center_y - Board.element_radius,
                center_x + 3 * Board.element_radius,
                center_y + Board.element_radius,
                width=0,
                fill=elements[1].color
            )
        elif n == 3:
            self.create_oval(
                center_x - Board.element_radius,
                int(center_y - 2.75 * Board.element_radius),
                center_x + Board.element_radius,
                int(center_y - 0.75 * Board.element_radius),
                width=0,
                fill=elements[0].color
            )
            self.create_oval(
                center_x - 3 * Board.element_radius,
                int(center_y + 0.75 * Board.element_radius),
                center_x - Board.element_radius,
                int(center_y + 2.75 * Board.element_radius),
                width=0,
                fill=elements[1].color
            )
            self.create_oval(
                center_x + Board.element_radius,
                int(center_y + 0.75 * Board.element_radius),
                center_x + 3 * Board.element_radius,
                int(center_y + 2.75 * Board.element_radius),
                width=0,
                fill=elements[2].color
            )
        elif n == 4 or n == 5:
            self.create_oval(
                center_x - 3 * Board.element_radius,
                center_y - 3 * Board.element_radius,
                center_x - Board.element_radius,
                center_y - Board.element_radius,
                width=0,
                fill=elements[0].color
            )
            self.create_oval(
                center_x + Board.element_radius,
                center_y - 3 * Board.element_radius,
                center_x + 3 * Board.element_radius,
                center_y - Board.element_radius,
                width=0,
                fill=elements[1].color
            )
            self.create_oval(
                center_x - 3 * Board.element_radius,
                center_y + Board.element_radius,
                center_x - Board.element_radius,
                center_y + 3 * Board.element_radius,
                width=0,
                fill=elements[2].color
            )
            self.create_oval(
                center_x + Board.element_radius,
                center_y + Board.element_radius,
                center_x + 3 * Board.element_radius,
                center_y + 3 * Board.element_radius,
                width=0,
                fill=elements[3].color
            )

            if n == 5:
                self.create_oval(
                    center_x - Board.element_radius,
                    center_y - Board.element_radius,
                    center_x + Board.element_radius,
                    center_y + Board.element_radius,
                    width=0,
                    fill=elements[4].color
                )

    def __get_map_left_upper_corner(self, center_at):
        # TODO: function to center map at player
        """x, y = center_at
        half_width = self.width // 2
        half_height = self.height // 2
        padding = {
            "left": half_width - 1 if is_even(self.width) else half_width,
            "right": half_width,
            "top": half_height - 1 if is_even(self.height) else half_height,
            "bottom": half_height
        }"""
