from .square_type import SquareType


class Shine(SquareType):
    def __init__(self):
        super().__init__(False)

    def getConsoleGraphic(self):
        return '*'
