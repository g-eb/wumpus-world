from .square_type import SquareType
from .shine import Shine


class NoGold(SquareType):
    color = "#ecc510"

    def __init__(self):
        super().__init__(False)
