from .square_type import SquareType
from .shine import Shine


class Gold(SquareType):
    color = "#fcc510"

    def __init__(self):
        super().__init__(False)

    def getEffect(self):
        return Shine()
