from .square_type import SquareType


class NoDragon(SquareType):
    color = "#baf409"

    def __init__(self):
        super().__init__(False)
