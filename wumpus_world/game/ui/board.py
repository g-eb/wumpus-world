from tkinter import Canvas, CENTER


class Board(Canvas):
    """A class representing the board."""

    square_size = 64
    square_spacing = 2
    square_element_radius = 8
    square_background_color = "#2f333d"
    board_background_color = "#282c34"
    board_padding = 8

    def __init__(self, map, master=None):
        """Creates a new board component from the tk.Canvas element."""

        super().__init__(
            master,
            background=Board.board_background_color,
            # This removes the default border around the canvas.
            highlightthickness=0
        )

        self.map = map
        self.width = map.width
        self.height = map.height

        self.__configure_size()
        # Center the board horizontally and vertically.
        self.place(relx=0.5, rely=0.5, anchor=CENTER)

    def render(self):
        """Renders all squares and their elements."""

        # Firstly clear all previously rendered squares to avoid memory leaks.
        self.delete("all")

        for y in range(self.height):
            for x in range(self.width):
                left_upper_vertex = self.__get_square_point(x, y)

                self.create_rectangle(
                    left_upper_vertex[0],
                    left_upper_vertex[1],
                    left_upper_vertex[0] + Board.square_size,
                    left_upper_vertex[1] + Board.square_size,
                    width=0,
                    fill=Board.square_background_color
                )

                # TODO: store (x, y) of a square inside Square class.
                self.__render_square_elements(x, y, self.map.squares[y][x])

    def __configure_size(self):
        """Sets the size of the board based on the window and map sizes.

        The board size is found as follows.
        Given the map width (mw), the map height (mh), a padding of the board
        (p), spacing between squares (s) and the sqaure size (a) the board
        width (bw) and the board height (bh) can be calculated using formulas:
                bw = mw * a + (mw - 1) * s + 2p
                   = mw * (a + s) + 2p - s
                bh = mh * a + (mh - 1) * s + 2p
                   = mh * (a + s) + 2p - s

        Let w be the width of the window and h be the height of the window.
        Following image shows all of the given sizes.

             ┌─────────────────────────────── w ──────────────────────────────┐
             │                                                                │
        ┌────╆━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┪
        │    ┃           ┌────────────────── bw ─────────────────┐            ┃
        │    ┃           ├─ p ┐    ┌─s┐                          │            ┃
        │    ┃     ┌──┬──╆━━━━┷━━━━┷━━┷━━━━━━━━━━━━━━━━━━━━━━━━━━┪            ┃
        │    ┃     │  p  ┃                                       ┃            ┃
        │    ┃     │  └──┨    ┏━━━━┓  ┏━━━━┓  ┏━━━━┓  ┏━━━━┓     ┃            ┃
        │    ┃     │     ┃    ┃    ┃  ┃    ┃  ┃    ┃  ┃    ┃     ┃            ┃
        │    ┃     │   ┌─┨    ┗━━━━┛  ┗━━━━┛  ┗━━━━┛  ┗━━━━┛     ┃            ┃
             ┃         s─┨    ┏━━━━┓  ┏━━━━┓  ┏━━━━┓  ┏━━━━┓     ┃            ┃
        h    ┃     bh    ┃    ┃    ┃  ┃    ┃  ┃    ┃  ┃    ┃     ┃            ┃
             ┃           ┃    ┗━━━━┛  ┗━━━━┛  ┗━━━━┛  ┗━━━━┛     ┃            ┃
        │    ┃     │     ┃    ┏━━━━┓  ┏━━━━┓  ┏━━━━┓  ┏━━━━┱──┐  ┃            ┃
        │    ┃     │     ┃    ┃    ┃  ┃    ┃  ┃    ┃  ┃    ┃  a  ┃            ┃
        │    ┃     │     ┃    ┗━━━━┛  ┗━━━━┛  ┗━━━━┛  ┡━━━━╃──┘  ┃            ┃
        │    ┃     │     ┃                            └ a ─┘     ┃            ┃
        │    ┃     └─────┺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛            ┃
        │    ┃                                                                ┃
        │    ┃                                                                ┃
        └────┺━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

        The board must fit in the window in such a way that no square can be
        cropped and the board must not have size larger than the map. If it is
        possible to display the full map within the window, it must be fully
        displayed.

        Firstly, find the maximum number of the uncropped squares that fit in
        the maximized board:
                w = nw * (a + s) + 2p - s =>
            => nw = floor((w + s - 2p) / (a + s))
                h = nh * (a + s) + 2p - s =>
            => nh = floor((h + s - 2p) / (a + s)),
        where nw and nh are the maximum numbers of the uncropped squares that
        fit in the window width and the window height respectively.

        If the map sizes aren't greater than these sizes, calculate bw and bh.
        Otherwise, calculate bw and bh as if the found maximum numbers of the
        uncropped squares were the map size.
        """

        window_width = self.master.width
        window_height = self.master.height
        map_width = self.map.width
        map_height = self.map.height
        doubled_padding = 2 * Board.board_padding
        spacing_without_padding = Board.square_spacing - doubled_padding
        square_with_spacing = Board.square_size + Board.square_spacing
        nw = (window_width + spacing_without_padding) // square_with_spacing
        nh = (window_height + spacing_without_padding) // square_with_spacing

        if map_width <= nw and map_height <= nh:
            # 2p - s = - (s - 2p)
            bw = map_width * square_with_spacing - spacing_without_padding
            bh = map_height * square_with_spacing - spacing_without_padding
        else:
            bw = nw * square_with_spacing - spacing_without_padding
            bh = nh * square_with_spacing - spacing_without_padding

        self.configure(width=bw, height=bh)

    def __get_square_point(self, x, y, center=False):
        """Returns coordinates of the left upper vertex of the square.

        If center is True, then returns the center of the square.
        """

        square_with_spacing = Board.square_size + Board.square_spacing
        left_upper_point = (
            Board.board_padding + x * square_with_spacing,
            Board.board_padding + y * square_with_spacing
        )

        if center:
            return (
                left_upper_point[0] + Board.square_size / 2,
                left_upper_point[1] + Board.square_size / 2
            )

        return left_upper_point

    def __render_square_elements(self, x, y, square):
        """Renders all elements that are at a given square.

        If there's only one element, it is drawn at the center of the square.

        If there are two elements, they are drawn as a horizontal line through
        the center of the square.

        For any greater number of the elements they are drawn as vertices of a
        regular polygon. Even-sided polygons are additionally rotated by a half
        of their exterior angle.
        """

        if len(square.contains) < 1:
            return

        # Sort elements by their class name so they are consistently shown.
        elements = sorted(
            square.contains, key=lambda el: el.__class__.__name__
        )
        n = len(elements)
        center = self.__get_square_point(x, y, center=True)

        if n == 1:
            # Draw at the center of the square.
            self.__draw_point(center, elements[0].color)

            return

        if n == 2:
            # Draw as a horizontal line through the center of the square.
            self.__draw_point(
                (center[0] - 2 * Board.square_element_radius, center[1]),
                elements[0].color
            )
            self.__draw_point(
                (center[0] + 2 * Board.square_element_radius, center[1]),
                elements[1].color
            )

            return

        # Draw as vertices of a regular polygon.
        start = (center[0], center[1] - 2 * Board.square_element_radius)
        alpha = 360 / n

        if n % 2 == 0:
            # Rotate an even-sided polygon.
            start = self.__rotate_point(
                start, center, alpha / 2, in_degrees=True)

        for index, element in enumerate(elements):
            point = self.__rotate_point(
                start, center, alpha * index, in_degrees=True)

            self.__draw_point(point, element.color)

    def __draw_point(self, point, color):
        """Draws a point as a circle with the Board.element_radius radius."""

        self.create_oval(
            round(point[0] - Board.square_element_radius),
            round(point[1] - Board.square_element_radius),
            round(point[0] + Board.square_element_radius),
            round(point[1] + Board.square_element_radius),
            width=0,
            fill=color
        )

    def __rotate_point(self, point, circle_center, angle, in_degrees=False):
        """Rotates a point on a circle by a given angle.

        Details about the derivation of a formula can be found at the website
        https://math.stackexchange.com/questions/1384994/rotate-a-point-on-a-circle-with-known-radius-and-position.
        """

        from math import sin, cos, radians

        if in_degrees:
            angle = radians(angle)

        sin_alpha = sin(angle)
        cos_alpha = cos(angle)
        diff = (point[0] - circle_center[0], point[1] - circle_center[1])

        return (
            circle_center[0] + diff[0] * cos_alpha - diff[1] * sin_alpha,
            circle_center[1] + diff[0] * sin_alpha + diff[1] * cos_alpha
        )

    def __get_map_left_upper_corner(self, center_at):
        # TODO: a method to center the map at the player.
        pass
