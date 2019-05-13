from .square_type import SquareType


class Shine(SquareType):
    color = "#fff693"

    def __init__(self):
        super().__init__(False)
