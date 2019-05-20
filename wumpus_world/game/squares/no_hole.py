from .square_type import SquareType


class NoHole(SquareType):
    color = "#d9fffa"
    text = "%"

    def __init__(self):
        super().__init__(False)
