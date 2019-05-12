from .square_type import SquareType


class Shine(SquareType):
    color = "#f7e594"
    symbol = '*'

    def __init__(self):
        super().__init__(False)
