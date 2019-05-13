from .square_type import SquareType


class Wind(SquareType):
    color = "#acb7b6"

    def __init__(self):
        super().__init__(False)
