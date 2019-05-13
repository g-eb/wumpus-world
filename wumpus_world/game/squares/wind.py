from .square_type import SquareType


class Wind(SquareType):
    color = "#c0c0c0"

    def __init__(self):
        super().__init__(False)
