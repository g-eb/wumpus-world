from .square_type import SquareType


class Wind(SquareType):
    def __init__(self):
        super().__init__(False)

    def getConsoleGraphic(self):
        return 'w'
