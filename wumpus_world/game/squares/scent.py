from .square_type import SquareType


class Scent(SquareType):
    color = "#602e01"

    def __init__(self):
        super().__init__(False)
